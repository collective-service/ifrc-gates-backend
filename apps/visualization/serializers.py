from rest_framework import serializers
from .models import DataCountryLevelMostRecent, SourceListAgg


class DataCountryLevelMostRecentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataCountryLevelMostRecent
        fields = '__all__'


class SourceListAggSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceListAgg
        fields = '__all__'
