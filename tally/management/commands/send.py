from django.core.management.base import BaseCommand
import tally

class Command (BaseCommand):

    def handle(self, *args, **options):
        tally.tally(*args)
