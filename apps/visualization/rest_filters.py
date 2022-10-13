from django_filters import rest_framework as filters
from .models import (
    DataCountryLevelMostRecent,
    DataCountryLevelPublic,
    DataGranularPublic,
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


class DataCountryLevelPublicFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3')
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = DataCountryLevelPublic
        fields = ()


class DataGranularPublicFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3')
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = DataGranularPublic
        fields = ()


class ContextualDataFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3')
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = ContextualData
        fields = ()
