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


class BaseExportFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3')
    include_header = filters.BooleanFilter(method='filter_include_header', required=True)

    def filter_include_header(self, queryset, name, value):
        # Used for browseable api documentation
        return queryset


class DataCountryLevelPublicExportFilter(BaseExportFilter):
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = DataCountryLevelPublic
        fields = ()


class DataGranularPublicExportFilter(BaseExportFilter):
    indicator_id = filters.CharFilter(field_name='indicator_id')

    class Meta:
        model = DataGranularPublic
        fields = ()


class ContextualDataExportFilter(BaseExportFilter):
    context_indicator_id = filters.CharFilter(field_name='context_indicator_id')

    class Meta:
        model = ContextualData
        fields = ()
