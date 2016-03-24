from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import collections
import sqlite3
import logging
import os
import re

logger = logging.getLogger(__name__)

if not hasattr(settings, 'TALLY_DATA_DIR'):
    raise ImproperlyConfigured('You must specify a TALLY_DATA_DIR setting to use tally.')

def get_bucket(timestamp, resolution):
    """ Normalize the timestamp to the given resolution. """
    return resolution * (int(timestamp) // resolution)

def inserts(rows, resolution):
    """ Yields the name and timestamp bucket for the INSERT statement in Archive.store. """
    for name, _value, timestamp in rows:
        yield name, get_bucket(timestamp, resolution)

def updates(rows, resolution):
    """ Yields parameters appropriate for the UPDATE statement in Archive.store. """
    for name, value, timestamp in rows:
        yield value, value, value, value, name, get_bucket(timestamp, resolution)

def matches(rows, pattern):
    """ Yields rows matching the specified glob pattern. """
    regex = pattern.replace('.', '\\.').replace('*', '.*')
    for name, value, timestamp in rows:
        # Short-circuit the regex match for * patterns.
        if pattern == '*' or re.match(regex, name, re.I):
            yield name, value, timestamp

class Archive (models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    pattern = models.CharField(max_length=100, default='*')
    resolution = models.IntegerField(default=5, help_text='Resolution in seconds.')
    retention = models.IntegerField(default=24, help_text='Retention period in hours.')
    enabled = models.BooleanField(default=True)

    db_path = property(lambda self: os.path.join(settings.TALLY_DATA_DIR, '%s.db' % self.slug))

    class Meta:
        ordering = ('retention', 'resolution')

    @property
    def data_points(self):
        return int((self.retention * 60 * 60) / self.resolution)

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
        self.create_if_needed()
        # Limit the rows to those matching our pattern.
        rows = list(matches(rows, self.pattern))
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

    def trim(self):
        """
        Removes any data points older than the retention time of the archive. The cutoff time is relative
        to the latest timestamp in the database, not the current time.
        """
        with self.database as db:
            last = db.execute('SELECT max(timestamp) FROM data').fetchone()[0]
            cutoff = int(last) - (self.retention * 60 * 60)
            return db.execute('DELETE FROM data WHERE timestamp < ?', (cutoff,)).rowcount

    def where(self, pattern=None, since=None, until=None, aggregate=None, low=None, high=None):
        sql = ''
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
            params.append(until)
        if aggregate and low is not None:
            clauses.append('agg_%s >= ?' % aggregate)
            params.append(float(low))
        if aggregate and high is not None:
            clauses.append('agg_%s <= ?' % aggregate)
            params.append(float(high))
        if clauses:
            sql = ' WHERE ' + ' AND '.join(clauses)
        return sql, params

    def values(self, pattern=None, aggregate=None, by='time', since=None, until=None, low=None, high=None):
        data = collections.OrderedDict()
        where, params = self.where(pattern, since, until, aggregate=aggregate, low=low, high=high)
        sel = 'timestamp, name' if by == 'name' else 'name, timestamp'
        agg = 'agg_%s' % aggregate if aggregate else 'agg_count, agg_sum, agg_avg, agg_min, agg_max'
        sql = 'SELECT %s, %s FROM data%s ORDER BY %s' % (sel, agg, where, sel)
        for row in self.database.execute(sql, params):
            value = row[2] if aggregate else {'count': row[2], 'sum': row[3], 'avg': row[4], 'min': row[5], 'max': row[6]}
            data.setdefault(row[0], collections.OrderedDict())[row[1]] = value
        return data

    def aggregate(self, pattern=None, aggregate=None, by='time', since=None, until=None, low=None, high=None):
        data = collections.OrderedDict()
        where, params = self.where(pattern, since, until)
        sel = 'timestamp' if by == 'time' else 'name'
        aggs = ['sum(agg_count)', 'sum(agg_sum)', 'avg(agg_avg)', 'min(agg_min)', 'max(agg_max)']
        agg_index = {'count': 0, 'sum': 1, 'avg': 2, 'min': 3, 'max': 4}
        agg = aggs[agg_index[aggregate]] if aggregate else ', '.join(aggs)
        having = ''
        order = '1'
        if aggregate and (low is not None or high is not None):
            clauses = []
            if low is not None:
                clauses.append('%s >= ?' % agg)
                params.append(float(low))
            if high is not None:
                clauses.append('%s <= ?' % agg)
                params.append(float(high))
            having = ' HAVING ' + ' AND '.join(clauses)
        if aggregate:
            order = '2 DESC, 1'
        sql = 'SELECT %s, %s FROM data%s GROUP BY %s%s ORDER BY %s' % (sel, agg, where, sel, having, order)
        for row in self.database.execute(sql, params):
            value = row[1] if aggregate else {'count': row[1], 'sum': row[2], 'avg': row[3], 'min': row[4], 'max': row[5]}
            data[row[0]] = value
        return data

    def timedata(self, pattern=None, aggregate=None, by='time', since=None, until=None, low=None, high=None, default=None, reverse=False):
        data = self.aggregate(pattern=pattern, aggregate=aggregate, since=since, until=until, low=low, high=high)
        if data:
            latest = max(data.keys())
            earliest = latest - ((self.data_points - 1) * self.resolution)
            for i in range(self.data_points):
                if reverse:
                    t = latest - (i * self.resolution)
                else:
                    t = earliest + (i * self.resolution)
                yield t, data.get(t, default)
    
    def patterns(self, include_all=False, max_depth=3):
        patterns = set()
        for row in self.database.execute('SELECT DISTINCT name FROM data'):
            if include_all:
                patterns.add(row[0])
            parts = row[0].split('.')
            while parts:
                parts.pop()
                if max_depth is None or len(parts) <= max_depth:
                    patterns.add('.'.join(parts) + '.*' if parts else '*')
        return list(sorted(patterns))
