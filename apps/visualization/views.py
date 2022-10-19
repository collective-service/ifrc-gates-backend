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


class ExportBaseView(ListAPIView):
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        return None

    def validate_export_params_together(self, params):
        query_params_keys_list = list(params.keys())
        if not any(elem in ['iso3', 'indicator_id'] for elem in query_params_keys_list):
            raise ValidationError({'error': 'iso3 or indicator_id params are required'})

        if 'limit' not in query_params_keys_list:
            raise ValidationError({'error': 'Limit is required.'})

        if 'offset' not in query_params_keys_list:
            raise ValidationError({'error': 'offset is required.'})

    def process_csv_response(self, header_fields, include_header, qs):
        response = HttpResponse(
            content_type='text/csv',
        )
        writer = csv.writer(response)

        if include_header:
            writer.writerow([field for field in header_fields])

        for item in qs:
            row = [getattr(item, field) for field in header_fields]
            writer.writerow(row)

        return response


class ExportRawDataView(ExportBaseView):

    filterset_class = DataGranularPublicExportFilter
    queryset = DataGranularPublic.objects.all()

    def get(self, request, format=None):
        """
        Export raw data
        """

        self.validate_export_params_together(self.request.query_params)
        filterset = DataGranularPublicExportFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        if filterset.is_valid():
            header_fields = [field.name for field in DataGranularPublic._meta.get_fields()]
            include_header = filterset.form.cleaned_data.get('include_header')
            return self.process_csv_response(header_fields, include_header, self.paginate_queryset(filterset.qs))


class ExportSummaryView(ExportBaseView):

    filterset_class = DataCountryLevelPublicExportFilter
    queryset = DataCountryLevelPublic.objects.all()

    def get(self, request, format=None):
        """
        Export summary data
        """

        self.validate_export_params_together(self.request.query_params)
        filterset = DataCountryLevelPublicExportFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        if filterset.is_valid():
            header_fields = [field.name for field in DataCountryLevelPublic._meta.get_fields()]
            include_header = filterset.form.cleaned_data.get('include_header')
            return self.process_csv_response(header_fields, include_header, self.paginate_queryset(filterset.qs))


class ExportCountryContextualDataView(ExportBaseView):

    filterset_class = ContextualDataExportFilter
    queryset = ContextualData.objects.all()

    def get(self, request, format=None):
        """
        Export country contextual data
        """

        self.validate_export_params_together(self.request.query_params)
        filterset = ContextualDataExportFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        if filterset.is_valid():
            header_fields = [field.name for field in ContextualData._meta.get_fields()]
            include_header = filterset.form.cleaned_data.get('include_header')
            return self.process_csv_response(header_fields, include_header, self.paginate_queryset(filterset.qs))
