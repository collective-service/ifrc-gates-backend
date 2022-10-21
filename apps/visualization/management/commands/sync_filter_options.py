from django.core.management.base import BaseCommand
from apps.visualization.models import DataCountryLevel
from apps.migrate_csv.models import CountryFilterOptions


class Command(BaseCommand):
    help = 'Command to sync distinct filter options'

    def handle(self, *args, **options):

        # Remove old filter options
        CountryFilterOptions.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Removed old filter options'))

        # Get distinct values queryset
        qs = DataCountryLevel.objects.values(
            'iso3', 'emergency', 'indicator_id', 'indicator_description', 'subvariable'
        ).distinct(
            'iso3', 'emergency', 'indicator_id', 'indicator_description', 'subvariable'
        )
        CountryFilterOptions.objects.bulk_create([
            CountryFilterOptions(
                iso3=item['iso3'],
                emergency=item['emergency'],
                indicator_id=item['indicator_id'],
                indicator_description=item['indicator_description'],
                subvariable=item['subvariable']
            ) for item in qs
        ])
        self.stdout.write(self.style.SUCCESS('Created %s distinct filter options' % qs.count()))
