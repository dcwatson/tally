__version_info__ = (0, 2, 0)
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
        host = getattr(settings, 'TALLY_HOST', '127.0.0.1')
    if port is None:
        port = getattr(settings, 'TALLY_PORT', 8900)
    prefix = getattr(settings, 'TALLY_PREFIX', '')
    parts = [prefix + str(name), str(value)]
    if timestamp:
        if hasattr(timestamp, 'timetuple'):
            timestamp = time.mktime(timestamp.timetuple())
        parts.append(str(int(timestamp)))
    TALLY_SOCKET.sendto(' '.join(parts), (host, port))
