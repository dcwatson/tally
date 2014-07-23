__version_info__ = (0, 3, 0)
__version__ = '.'.join(str(i) for i in __version_info__)

import socket
import time

try:
    from django.conf import settings
except ImportError:
    # Don't require Django if only using the UDP client.
    settings = None

TALLY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def tally(name, value=1, timestamp=None, host=None, port=None):
    """
    Sends a metric to the specified host:port
    """
    if host is None:
        host = getattr(settings, 'TALLY_HOST', None)
    if port is None:
        port = getattr(settings, 'TALLY_PORT', 8900)
    prefix = getattr(settings, 'TALLY_PREFIX', '')
    name = prefix + str(name)
    value = float(value)
    if timestamp:
        if hasattr(timestamp, 'timetuple'):
            timestamp = time.mktime(timestamp.timetuple())
        timestamp = int(timestamp)
    if host is None:
        # If no host is specified, assume the tally should be written to all Archives locally.
        from .models import Archive
        if timestamp is None:
            timestamp = int(time.time())
        rows = [(name, value, timestamp)]
        for a in Archive.objects.filter(enabled=True):
            a.store(rows)
            a.trim()
    else:
        # If a host and port are specified, send the tally in a UDP packet.
        parts = [name, str(value)]
        if timestamp:
            parts.append(str(timestamp))
        TALLY_SOCKET.sendto(' '.join(parts), (host, port))
