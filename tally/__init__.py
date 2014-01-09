__version_info__ = (0, 1, 0)
__version__ = '.'.join(str(i) for i in __version_info__)

from django.conf import settings
import socket
import time

TALLY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def tally(name, value=1, timestamp=None, host=None, port=None):
    if host is None:
        host = getattr(settings, 'TALLY_HOST', '127.0.0.1')
    if port is None:
        port = getattr(settings, 'TALLY_PORT', 8900)
    parts = [str(name), str(value)]
    if timestamp:
        if hasattr(timestamp, 'timetuple'):
            timestamp = time.mktime(timestamp.timetuple())
        parts.append(str(int(timestamp)))
    TALLY_SOCKET.sendto(' '.join(parts), (host, port))
