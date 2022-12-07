from django.conf import settings
import csv
from django.http import HttpResponse
from django.db.models import Max, Q
from functools import reduce
from rest_framework.exceptions import ValidationError
from django.db import connection
from django_redis import get_redis_connection
from rest_framework import response
from utils import str_to_bool
from .models import (
    DataCountryLevelMostRecent,
    DataCountryLevelPublic,
    DataGranularPublic,
    DataCountryLevelPublicContext,
)
from .serializers import DataCountryLevelMostRecentSerializer
from .rest_filters import (
    DataCountryLevelMostRecentFilter,
    BaseExportFilter,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


class ContextIndicatorsViews(ListAPIView):
    '''
    Returns most recent inidcator values for a country level.
    It accepts String query parameters such as emergency, region, iso3, type, thematic,
    topic as filter.
    It also accepts query parameters such as limit and offset to request number of objects
    in a page.
    Comma separated string query parameters can be given for topic to filter according
    to multiple topic.
    '''
    default_limit = 10
    serializer_class = DataCountryLevelMostRecentSerializer
    filterset_class = DataCountryLevelMostRecentFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.query_params.get('limit'):
            limit = int(self.request.query_params.get('limit'))
            if limit > settings.OPEN_API_MAX_PAGE_LIMIT:
                raise ValidationError(
                    {'error': f'Limit must be less or equal to {settings.OPEN_API_MAX_PAGE_LIMIT}'}
                )
        result = DataCountryLevelMostRecent.objects.filter(category='Global').order_by(
            '-indicator_month'
        ).values(
            'subvariable'
        ).annotate(
            max_indicator_month=Max('indicator_month'),
        )
        filters = reduce(lambda acc, item: acc | item, [
            Q(
                subvariable=value['subvariable'],
                indicator_month=value['max_indicator_month'],
            ) for value in result
        ])
        return DataCountryLevelMostRecent.objects.filter(filters).distinct('subvariable')


class ExportBaseView(ListAPIView):
    filterset_class = BaseExportFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        return None

    def validate_export_params_together(self, params):
        errors = []
        query_params_keys_list = list(params.keys())
        if not any(elem in ['iso3', 'indicator_id'] for elem in query_params_keys_list):
            errors.append('iso3 or indicator_id params are required')
        if 'limit' not in query_params_keys_list:
            errors.append('Limit is required.')
        if 'offset' not in query_params_keys_list:
            errors.append('offset is required.')
        limit = params.get('limit')
        if 'include_header' not in query_params_keys_list:
            errors.append('include_header bool param is required')
        if limit and int(limit) > settings.OPEN_API_MAX_EXPORT_PAGE_LIMIT:
            errors.append(
                f'Limit must be less or equal to {settings.OPEN_API_MAX_EXPORT_PAGE_LIMIT}'
            )
        if errors:
            raise ValidationError({'non_field_errors': errors})

    def process_csv_response(self, header_fields, include_header, qs):
        response = HttpResponse(
            content_type='text/csv',
        )
        writer = csv.writer(response)
        if include_header:
            writer.writerow(header_fields)
        for item in qs:
            row = [getattr(item, field) for field in header_fields]
            writer.writerow(row)
        return response

    def get(self, request, format=None):
        self.validate_export_params_together(self.request.query_params)
        filterset = self.filterset_class(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        if filterset.is_valid():
            header_fields = [field.name for field in filterset.qs.model._meta.get_fields()]
            include_header = str_to_bool(self.request.query_params.get('include_header'))
            return self.process_csv_response(header_fields, include_header, self.paginate_queryset(filterset.qs))


class ExportRawDataView(ExportBaseView):
    queryset = DataGranularPublic.objects.all()


class ExportSummaryView(ExportBaseView):
    queryset = DataCountryLevelPublic.objects.all()


class ExportCountryDataCountryLevelPublicContextView(ExportBaseView):
    queryset = DataCountryLevelPublicContext.objects.all()


class HealthCheckupView(APIView):

    def get(self, request):
        """
        Check database connection and redis
        """
        is_database_connected = connection.ensure_connection()
        is_redis_connected = get_redis_connection("default")
        # NOTE: if database is connected is_database_connected will return None
        if not is_database_connected and is_redis_connected:
            return response.Response({'message': 'OK'})
