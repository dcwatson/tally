from django.core.management.base import BaseCommand
import random
import tally
import time
import sys

class Command (BaseCommand):

    def handle(self, *args, **options):
        if len(args) != 3:
            print 'usage: flood <total_entries> <key_prefix> <key_count>'
            sys.exit(1)
        now = int(time.time())
        for _i in range(int(args[0])):
            key = '%s.%s' % (args[1], random.randint(1, int(args[2])))
            value = random.randint(1, 100)
            when = now - random.randint(0, 3600)
            tally.tally(key, value, when)
