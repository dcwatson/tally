from django.db import models
from django.conf import settings
from django.core.cache import cache
import sqlite3
import time
import os

def get_bucket(timestamp, resolution):
    """ Normalize the timestamp to the given resolution. """
    return resolution * (int(timestamp) // resolution)

def inserts(rows, resolution):
    """ Yields the name and timestamp bucket for the INSERT statement. """
    for name, value, timestamp in rows:
        yield name, get_bucket(timestamp, resolution)

def updates(rows, resolution):
    """ Yields parameters appropriate for the UPDATE statement. """
    for name, value, timestamp in rows:
        yield value, value, value, value, name, get_bucket(timestamp, resolution)

class Archive (models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    pattern = models.CharField(max_length=100, default='*')
    resolution = models.IntegerField(help_text='Resolution in seconds.')
    retention = models.IntegerField(help_text='Retention period in hours.')

    cache_key = property(lambda self: '%s-pending' % self.slug)
    db_path = property(lambda self: os.path.join(settings.TALLY_DATA_DIR, '%s.db' % self.slug))

    @property
    def database(self):
        if not getattr(self, '_db', None):
            self._db = sqlite3.connect(self.db_path)
        return self._db

    def save(self, **kwargs):
        self.create_if_needed()
        super(Archive, self).save(**kwargs)

    def create_if_needed(self):
        if not os.path.exists(settings.TALLY_DATA_DIR):
            os.makedirs(settings.TALLY_DATA_DIR)
        if not os.path.exists(self.db_path):
            self.database.execute("""
                CREATE TABLE data (
                    name text,
                    timestamp integer,
                    agg_count integer DEFAULT 0,
                    agg_sum real DEFAULT 0,
                    agg_avg real DEFAULT 0,
                    agg_min real DEFAULT 2147483647,
                    agg_max real DEFAULT -2147483648,
                    PRIMARY KEY (name, timestamp) ON CONFLICT IGNORE
                )
            """)

    def store(self, rows):
        if rows:
            # Executing paramaterized INSERTs/UPDATEs is faster inside a transaction.
            with self.database as db:
                # Make sure records with default values exist for any name/timestamp we're about to update.
                # The "ON CONFLICT IGNORE" part of the DDL is important here, so we don't need a separate check.
                db.executemany('INSERT INTO data (name, timestamp) VALUES (?, ?)', inserts(rows, self.resolution))
                # Run UPDATEs for all the values, recomputing the aggregates for the given name/timestamp.
                db.executemany("""
                    UPDATE data SET
                        agg_count = agg_count + 1,
                        agg_sum = agg_sum + ?,
                        agg_avg = (agg_sum + ?) / (agg_count + 1),
                        agg_min = min(agg_min, ?),
                        agg_max = max(agg_max, ?)
                    WHERE name = ? AND timestamp = ?
                """, updates(rows, self.resolution))
            return len(rows)
        return 0

    def values(self, pattern='*', aggregate='sum', since=None, until=None):
        names = {}
        where = "name LIKE '%s'" % pattern.replace('*', '%') if '*' in pattern else "name = '%s'" % pattern
        cursor = self.database.cursor()
        cursor.execute('SELECT name, timestamp, agg_%s FROM data WHERE %s' % (aggregate, where))
        for row in cursor.fetchall():
            names.setdefault(row[0], []).append((row[1], row[2]))
        cursor.close()
        return names
