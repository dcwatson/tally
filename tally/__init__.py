__version_info__ = (1, 0, 0)
__version__ = '.'.join(str(i) for i in __version_info__)

import socket
import time

try:
    from django.conf import settings
except:
    # Don't require Django if only using the UDP client.
    settings = None

TALLY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def archives():
    """
    Returns a QuerySet of all enabled Archives.
    """
    from .models import Archive
    return Archive.objects.filter(enabled=True)

def tally(data, value=1, timestamp=None, host=None, port=None):
    """
    Sends a metric to the specified host:port
    """
    if host is None:
        host = getattr(settings, 'TALLY_HOST', None)
    if port is None:
        port = getattr(settings, 'TALLY_PORT', 8900)
    prefix = unicode(getattr(settings, 'TALLY_PREFIX', ''))
    if not isinstance(data, (list, tuple)):
        data = [data]
    value = float(value)
    if timestamp:
        if hasattr(timestamp, 'timetuple'):
            timestamp = time.mktime(timestamp.timetuple())
        timestamp = int(timestamp)
    rows = []
    for d in data:
        row = []
        if isinstance(d, (list, tuple)):
            # First element is the metric name.
            if len(d) >= 1:
                name = unicode(d[0])
                if not name.startswith(prefix):
                    name = prefix + name
                row.append(name)
            else:
                # If we get an empty list or tuple, ignore it.
                continue
            # Second element is the value. Use the default if none specified.
            if len(d) >= 2:
                row.append(float(d[1]))
            else:
                row.append(value)
            # Third element is the timestamp. Use the default if none specified and host is None,
            # otherwise leave it off and only send the server name and value.
            if len(d) >= 3:
                row.append(int(d[2]))
            elif host is None:
                row.append(timestamp or int(time.time()))
        else:
            name = unicode(d)
            if not name.startswith(prefix):
                name = prefix + name
            row.append(name)
            row.append(value)
            # If recording directly to the database, Archive.store expects 3-tuples with a timestamp.
            # Otherwise, let the server use its local time.
            if host is None:
                row.append(timestamp or int(time.time()))
        rows.append(row)
    if host is None:
        # If no host is specified, assume the tallies should be written to all Archives locally.
        for a in archives():
            a.store(rows)
            a.trim()
    else:
        # If a host and port are specified, send the tallies in a UDP packet.
        lines = []
        for row in rows:
            lines.append(u' '.join(unicode(p) for p in row))
        TALLY_SOCKET.sendto(u'\n'.join(lines).encode('utf-8'), (host, port))
