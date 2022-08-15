from django import forms
from apps.migrate_csv.models import CsvFile
from django.forms import ValidationError
import pandas as pd


class CsvFileForm(forms.ModelForm):
    class Meta:
        model = CsvFile
        fields = '__all__'

    def valid_csv_fields(self):
        return {
            'outbreak',
            'country',
            'iso3',
            'adminlevel1',
            'indicator',
            'indicator_id',
            'questions',
            'percentage',
            'nominator',
            'denominator',
            'gender',
            'age_group',
            'age_info',
            'target_group',
            'date',
            'contribution_marker',
            'errormargin',
            'representativeness',
            'area',
            'limitation',
            'comment',
            'source_id',
            'topic',
            'thematic',
            'subindicator',
        }

    def _validate_csv_file_with_headers(self):
        file = self.cleaned_data.get('file', None)
        if not file:
            raise ValidationError('File is required.')

        if not file.name.endswith('.csv'):
            raise ValidationError('File format should be csv.')

        # Calculate diff between exising fields and imported csv columns
        csv_headers = pd.read_csv(file, delimiter=',').columns.values
        csv_headers_set = {x.strip().lower().replace(" ", "_") for x in csv_headers}
        diff = csv_headers_set.difference(self.valid_csv_fields())
        diff2 = self.valid_csv_fields().difference(csv_headers_set)
        if diff:
            raise ValidationError(f'Following columns mismatched {diff}')
        if diff2:
            raise ValidationError(f'Following columns mismatched {diff2}')

    def clean(self):
        self._validate_csv_file_with_headers()
        return self.cleaned_data
