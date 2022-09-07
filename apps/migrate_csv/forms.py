from django import forms
from apps.migrate_csv.models import DataImport


class DataImportForm(forms.ModelForm):
    class Meta:
        model = DataImport
        fields = '__all__'
