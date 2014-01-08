import socket
import time

TALLY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def tally(name, value=1, timestamp=None, host='127.0.0.1', port=8900):
    parts = [str(name), str(value)]
    if timestamp:
        if hasattr(timestamp, 'timetuple'):
            timestamp = time.mktime(timestamp.timetuple())
        parts.append(str(int(timestamp)))
    TALLY_SOCKET.sendto(' '.join(parts), (host, port))
