from rest_framework import serializers
from .models import DataCountryLevelMostRecent


class DataCountryLevelMostRecentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataCountryLevelMostRecent
        fields = '__all__'
