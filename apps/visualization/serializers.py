from rest_framework import serializers
from .models import DataCountryLevelMostRecent


class DataCountryLevelMostRecentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataCountryLevelMostRecent
        fields = [
            'emergency', 'iso3', 'country_name', 'region', 'indicator_name',
            'indicator_value', 'indicator_month', 'type', 'thematic', 'topic', 'subvariable', 'category'
            ]
