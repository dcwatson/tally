# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings
import threading
import functools
import shutil
import Queue

from tally.management.commands.tallyserver import listener, flusher
import tally

class TallyTests (TestCase):
    fixtures = ('archives.json',)

    def setUp(self):
        pass

    def tearDown(self):
        try:
            shutil.rmtree(settings.TALLY_DATA_DIR)
        except:
            pass

    def test_unicode(self):
        self.assertEqual(tally.archives().count(), 3)
        tally.tally(u'ƒünk¥', 1000)
        tally.tally(u'ƒünk¥', 337)
        data = tally.archives().first().aggregate(by='name')
        self.assertIn(u'ƒünk¥', data)
        self.assertEqual(data[u'ƒünk¥']['count'], 2)
        self.assertEqual(data[u'ƒünk¥']['sum'], 1337)

class SocketTests (TestCase):
    fixtures = ('archives.json',)

    def _broken_test(self):
        queue = Queue.Queue()
        kill = threading.Event()
        listen = threading.Thread(target=functools.partial(listener, queue, kill))
        flush = threading.Thread(target=functools.partial(flusher, queue, kill, 1.0))
        listen.start()
        flush.start()
        # TODO: figure out why the flusher thread can't access the database.
        kill.set()
        flush.join()
        listen.join()
