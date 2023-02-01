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
        qs = super().qs
        date_from = self.data.get('date_from')
        date_to = self.data.get('date_to')

        if not (date_from or date_to):
            latest_date_object = qs.order_by('-insert_date').first()
            if latest_date_object:
                latest_insert_date = latest_date_object.insert_date
                date_before_7_days = latest_insert_date - timedelta(days=7)
                return qs.filter(insert_date__gte=date_before_7_days)
        return qs


class BaseExportFilter(filters.FilterSet):
    iso3 = filters.CharFilter(field_name='iso3')
    indicator_id = filters.CharFilter(field_name='indicator_id')
