from django.core.management.base import BaseCommand
from django.conf import settings
from tally.models import Archive
import threading
import functools
import logging
import socket
import Queue
import time

logger = logging.getLogger(__name__)

def listener(queue, kill):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = getattr(settings, 'TALLY_HOST', '127.0.0.1')
    port = getattr(settings, 'TALLY_PORT', 8900)
    sock.bind((host, port))
    sock.settimeout(1.0)
    while not kill.is_set():
        try:
            data, _addr = sock.recvfrom(1024)
            parts = data.split()[:3]
            parts[1] = float(parts[1])
            if len(parts) > 2:
                # If a timestamp was sent in, use it.
                parts[2] = int(float(parts[2]))
            else:
                # Otherwise, grab the current time and use that.
                parts.append(int(time.time()))
            queue.put(parts)
        except socket.timeout:
            pass
        except:
            pass

def flusher(queue, kill):
    flush_time = getattr(settings, 'TALLY_FLUSH_TIME', 5.0)
    while not kill.is_set():
        start = time.time()
        rows = []
        try:
            while True:
                rows.append(queue.get_nowait())
        except Queue.Empty:
            pass
        if rows:
            for a in Archive.objects.all():
                s = time.time()
                num = a.store(rows)
                deleted = a.trim()
                if num:
                    logger.debug('Inserted %d into, and deleted %d from, archive "%s" in %fs', num, deleted, a, time.time() - s)
            logger.debug('Finished flush of %d record(s) in %fs', len(rows), time.time() - start)
        time.sleep(flush_time)

class Command (BaseCommand):

    def handle(self, *args, **options):
        queue = Queue.Queue()
        kill = threading.Event()
        threading.Thread(target=functools.partial(listener, queue, kill)).start()
        threading.Thread(target=functools.partial(flusher, queue, kill)).start()
        while not kill.is_set():
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                print 'Shutting down...'
                kill.set()
