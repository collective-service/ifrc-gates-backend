from django_filters import rest_framework as filters
from .models import (
    DataCountryLevelMostRecent,
    DataCountryLevel,
    DataGranular,
    ContextualData,
)


class DataCountryLevelMostRecentFilter(filters.FilterSet):
    emergency = filters.CharFilter(field_name='emergency')
    region = filters.CharFilter(field_name='region')
    iso3 = filters.CharFilter(field_name='iso3')
    type = filters.CharFilter(field_name='type')
    thematic = filters.CharFilter(field_name='thematic')
    topic = filters.CharFilter(field_name='topic', method='filter_topic')

    class Meta:
        model = DataCountryLevelMostRecent
        fields = ()

    def filter_topic(self, qs, name, value):
        if not value:
            return qs
        topics = [topic.lstrip() for topic in value.split(',')]
        return qs.filter(topic__in=topics)


class DataCountryLevelFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3', required=True)
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = DataCountryLevel
        fields = ()


class DataGranularFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3', required=True)
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = DataGranular
        fields = ()


class ContextualDataFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3', required=True)
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = ContextualData
        fields = ()
