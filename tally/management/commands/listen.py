from django.core.management.base import BaseCommand
from django.conf import settings
from tally.models import Archive
import threading
import functools
import socket
import Queue
import time

def listener(queue, kill):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 8900))
    sock.settimeout(1.0)
    while not kill.is_set():
        try:
            data, _addr = sock.recvfrom(1024)
            parts = data.split()
            parts[1] = float(parts[1])
            if len(parts) > 2:
                parts[2] = int(float(parts[2]))
            else:
                parts.append(int(time.time()))
            queue.put(parts)
        except socket.timeout:
            pass
        except:
            pass

def flusher(queue, kill):
    while not kill.is_set():
        rows = []
        try:
            while True:
                rows.append(queue.get_nowait())
        except Queue.Empty:
            pass
        for a in Archive.objects.all():
            a.store(rows)
        time.sleep(settings.TALLY_FLUSH_TIME)

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
