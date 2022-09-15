from django.db.models import Q
from rest_framework import (
    viewsets,
)

from .models import DataCountryLevelMostRecent
from .serializers import DataCountryLevelMostRecentSerializer
from .rest_filters import DataCountryLevelMostRecentFilter


class DataCountryLevelMostRecentViewset(viewsets.ReadOnlyModelViewSet):
    queryset = DataCountryLevelMostRecent.objects.filter(category='Global').order_by('-indicator_month')
    serializer_class = DataCountryLevelMostRecentSerializer
    filterset_class = DataCountryLevelMostRecentFilter

    def get_queryset(self):
        search_params = self.request.query_params.get('search', None)
        if search_params:
            search_list = search_params.replace(" ", "").split(',')
            return self.queryset.filter(
                Q(emergency__in=search_list) |
                Q(iso3__in=search_list) |
                Q(type__in=search_list) |
                Q(thematic__in=search_list) |
                Q(topic__in=search_list) |
                Q(iso3__in=search_list) |
                Q(country_name__in=search_list) |
                Q(indicator_id__in=search_list) |
                Q(subvariable__in=search_list) |
                Q(indicator_name__in=search_list)
            )
        else:
            return self.queryset
