from django.db.models import Max, F
from rest_framework import (
    views,
)

from .models import DataCountryLevelMostRecent
from .serializers import DataCountryLevelMostRecentSerializer
from rest_framework.pagination import LimitOffsetPagination


class ContextIndicatorsViews(views.APIView, LimitOffsetPagination):
    default_limit = 10

    def get(self, request):

        emergency = request.query_params.get('emergency', None)
        region = request.query_params.get('region', None)
        iso3 = request.query_params.get('iso3', None)
        type = request.query_params.get('type', None)
        thematic = request.query_params.get('thematic', None)
        topic = request.query_params.get('topic', None)
        all_filters = {
            'emergency': emergency,
            'region': region,
            'iso3': iso3,
            'type': type,
            'thematic': thematic,
            'topic': topic,
        }
        data_country_filters = {k: v for k, v in all_filters.items() if v is not None}

        result = DataCountryLevelMostRecent.objects.filter(
            category='Global',
            **data_country_filters
        ).order_by(
            '-indicator_month'
        ).values(
            'subvariable'
        ).annotate(
            indicator_name=F('indicator_name'),
            indicator_month=Max('indicator_month'),
            category=F('category'),
            emergency=F('emergency'),
            indicator_value=F('indicator_value'),
            iso3=F('iso3'),
            type=F('type'),
            thematic=F('thematic'),
            topic=F('topic')
        )

        results = self.paginate_queryset(result, request, view=self)

        serializer = DataCountryLevelMostRecentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
