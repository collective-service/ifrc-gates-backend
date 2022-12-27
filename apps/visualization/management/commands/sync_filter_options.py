from django.core.management.base import BaseCommand
from utils import update_filter_options


class Command(BaseCommand):
    help = 'Command to sync distinct filter options'

    def handle(self, *args, **options):
        count = update_filter_options()
        self.stdout.write(self.style.SUCCESS('Created %s distinct filter options' % count))
