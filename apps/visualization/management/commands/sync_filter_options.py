from django.core.management.base import BaseCommand
from apps.visualization.models import DataCountryLevel
from apps.migrate_csv.models import CachedCountryFilterOptions


class Command(BaseCommand):
    help = 'Command to sync distinct filter options'

    def handle(self, *args, **options):

        # Remove old filter options
        CachedCountryFilterOptions.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Removed old filter options'))

        # Get distinct values queryset
        qs = DataCountryLevel.objects.values(
            'iso3', 'emergency', 'indicator_id', 'indicator_description', 'subvariable', 'type',
        ).distinct(
            'iso3', 'emergency', 'indicator_id', 'indicator_description', 'subvariable', 'type',
        )
        CachedCountryFilterOptions.objects.bulk_create([
            CachedCountryFilterOptions(
                iso3=item['iso3'],
                emergency=item['emergency'],
                indicator_id=item['indicator_id'],
                indicator_description=item['indicator_description'],
                subvariable=item['subvariable'],
                type=item['type'],
            ) for item in qs
        ])
        self.stdout.write(self.style.SUCCESS('Created %s distinct filter options' % qs.count()))
