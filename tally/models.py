from django.db import models
from django.conf import settings
import collections
import sqlite3
import os
import re

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

def matches(rows, pattern):
    regex = pattern.replace('.', '\\.').replace('*', '.*')
    for name, value, timestamp in rows:
        # Short-circuit the regex match for * patterns.
        if pattern == '*' or re.match(regex, name, re.I):
            yield name, value, timestamp

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

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        self.create_if_needed()
        super(Archive, self).save(**kwargs)

    def get_absolute_url(self):
        return '/archive/%s/' % self.slug

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
            # Limit the rows to those matching our pattern.
            rows = list(matches(rows, self.pattern))
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

    def values(self, pattern=None, aggregate=None, by='time', since=None, until=None):
        data = collections.OrderedDict()
        clauses = []
        params = []
        if pattern:
            if '*' in pattern:
                clauses.append('name LIKE ?')
                params.append(pattern.replace('*', '%'))
            else:
                clauses.append('name = ?')
                params.append(pattern)
        if since:
            clauses.append('timestamp >= ?')
            params.append(since)
        if until:
            clauses.append('timestamp <= ?')
            params.append(since)
        sel = 'timestamp, name' if by == 'name' else 'name, timestamp'
        agg = 'agg_%s' % aggregate if aggregate else 'agg_count, agg_sum, agg_avg, agg_min, agg_max'
        where = 'WHERE ' + ' AND '.join(clauses) if clauses else ''
        sql = 'SELECT %s, %s FROM data %s ORDER BY %s' % (sel, agg, where, sel)
        cursor = self.database.cursor()
        cursor.execute(sql, params)
        for row in cursor.fetchall():
            value = row[2] if aggregate else {'count': row[2], 'sum': row[3], 'avg': row[4], 'min': row[5], 'max': row[6]}
            data.setdefault(row[0], collections.OrderedDict())[row[1]] = value
        cursor.close()
        return data
