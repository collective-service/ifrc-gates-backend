from datetime import timedelta
from django_filters import rest_framework as filters
from .models import (
    DataCountryLevelMostRecent,
    SourceListAgg,
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


class SourceListAggFilter(filters.FilterSet):
    emergency = filters.CharFilter(field_name='emergency')
    iso3 = filters.CharFilter(field_name='iso3', method='filter_iso3')
    date_from = filters.DateFilter(field_name="source_date", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="source_date", lookup_expr='lte')

    class Meta:
        model = SourceListAgg
        fields = ()

    def filter_iso3(self, qs, name, value):
        if not value:
            return qs
        return qs.filter(iso3__icontains=value)

    @property
    def qs(self):
        parent = super().qs

        query_params = [k for k in self.request.query_params]
        # For date range, if not mentioned, default action is to pull the data from the last 7 days.
        if any(item in query_params for item in ['date_from', 'date_to']):
            return parent

        latest_insert_date = SourceListAgg.objects.all().order_by('-insert_date').first().insert_date
        date_before_7_days = latest_insert_date - timedelta(days=7)
        return parent.filter(insert_date__gte=date_before_7_days)


class BaseExportFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3')
    indicator_id = filters.CharFilter(field_name='indicator_id')
