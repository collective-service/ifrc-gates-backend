from django.conf import settings
import csv
from django.http import HttpResponse
from django.db.models import Max, Q
from functools import reduce
from rest_framework.exceptions import ValidationError
from .models import (
    DataCountryLevelMostRecent,
    DataCountryLevelPublic,
    DataGranularPublic,
    ContextualData,
)
from .serializers import DataCountryLevelMostRecentSerializer
from .rest_filters import (
    DataCountryLevelMostRecentFilter,
    DataCountryLevelPublicExportFilter,
    DataGranularPublicExportFilter,
    ContextualDataExportFilter,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView


def validate_export_params_together(params):
    if not any(elem in ['iso3', 'indicator_id'] for elem in list(params.keys())):
        raise ValidationError({'error': 'iso3 or indicator_id params are required'})


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
        result = DataCountryLevelMostRecent.filter(category='Global').objects.order_by(
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


class ExportRawDataView(ListAPIView):

    filterset_class = DataGranularPublicExportFilter
    queryset = DataGranularPublic.objects.all()

    def get(self, request, format=None):
        """
        Export raw data
        """

        validate_export_params_together(self.request.query_params)
        filterset = DataGranularPublicExportFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="raw-data.csv"'},
        )
        writer = csv.writer(response)
        all_fields = [field.name for field in DataGranularPublic._meta.get_fields()]
        writer.writerow(all_fields)
        for item in filterset.qs:
            row = [getattr(item, field) for field in all_fields]
            writer.writerow(row)
        return response


class ExportSummaryView(ListAPIView):

    filterset_class = DataCountryLevelPublicExportFilter
    queryset = DataCountryLevelPublic.objects.all()

    def get(self, request, format=None):
        """
        Export summary data
        """

        validate_export_params_together(self.request.query_params)
        filterset = DataCountryLevelPublicExportFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="summary.csv"'},
        )
        writer = csv.writer(response)
        all_fields = [field.name for field in DataCountryLevelPublic._meta.get_fields()]
        writer.writerow(all_fields)
        for item in filterset.qs:
            row = [getattr(item, field) for field in all_fields]
            writer.writerow(row)
        return response


class ExportCountryContextualDataView(ListAPIView):

    filterset_class = ContextualDataExportFilter
    queryset = ContextualData.objects.all()

    def get(self, request, format=None):
        """
        Export country contextual data
        """

        validate_export_params_together(self.request.query_params)
        filterset = ContextualDataExportFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="country-contextual-data.csv"'},
        )
        writer = csv.writer(response)

        all_fields = [field.name for field in ContextualData._meta.get_fields()]
        writer.writerow(all_fields)
        for item in filterset.qs:
            row = [getattr(item, field) for field in all_fields]
            writer.writerow(row)
        return response
