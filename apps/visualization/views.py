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
    DataCountryLevelPublicFilter,
    DataGranularPublicFilter,
    ContextualDataFilter,
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

    filterset_class = DataGranularPublicFilter
    queryset = DataGranularPublic.objects.all()

    def get(self, request, format=None):
        """
        Export raw data
        """

        validate_export_params_together(self.request.query_params)
        filterset = DataGranularPublicFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="raw-data.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow([
            'emergency',
            'country_name',
            'region',
            'iso3',
            'admin_level_1',
            'indicator_id',
            'subvariable',
            'indicator_name',
            'thematic',
            'thematic_description',
            'topic',
            'topic_description',
            'indicator_description',
            'type',
            'question',
            'indicator_value',
            'nominator',
            'error_margin',
            'denominator',
            'indicator_month',
            'category',
            'gender',
            'age_group',
            'age_info',
            'target_group',
            'indicator_matching',
            'representativeness',
            'limitation',
            'indicator_comment',
            'source_id',
            'organisation',
            'title',
            'details',
            'authors',
            'methodology',
            'sample_size',
            'target_pop',
            'scale',
            'quality_check',
            'access_type',
            'source_comment',
            'publication_channel',
            'link',
            'source_date',
            'sample_type',
        ])
        for item in filterset.qs:
            writer.writerow([
                item.emergency,
                item.country_name,
                item.region,
                item.iso3,
                item.admin_level_1,
                item.indicator_id,
                item.subvariable,
                item.indicator_name,
                item.thematic,
                item.thematic_description,
                item.topic,
                item.topic_description,
                item.indicator_description,
                item.type,
                item.question,
                item.indicator_value,
                item.nominator,
                item.error_margin,
                item.denominator,
                item.indicator_month,
                item.category,
                item.gender,
                item.age_group,
                item.age_info,
                item.target_group,
                item.indicator_matching,
                item.representativeness,
                item.limitation,
                item.indicator_comment,
                item.source_id,
                item.organisation,
                item.title,
                item.details,
                item.authors,
                item.methodology,
                item.sample_size,
                item.target_pop,
                item.scale,
                item.quality_check,
                item.access_type,
                item.source_comment,
                item.publication_channel,
                item.link,
                item.source_date,
                item.sample_type,
            ])
        return response


class ExportSummaryView(ListAPIView):

    filterset_class = DataCountryLevelPublicFilter
    queryset = DataCountryLevelPublic.objects.all()

    def get(self, request, format=None):
        """
        Export summary data
        """

        validate_export_params_together(self.request.query_params)
        filterset = DataCountryLevelPublicFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="summary.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow([
            'emergency',
            'country_name',
            'iso3',
            'admin_level_1',
            'region',
            'income_group',
            'fragility_index_fund_for_peace',
            'population_size',
            'indicator_id',
            'subvariable',
            'indicator_name',
            'thematic',
            'thematic_description',
            'topic',
            'topic_description',
            'indicator_description',
            'type',
            'indicator_value',
            'error_margin',
            'indicator_month',
            'category',
        ])
        for item in filterset.qs:
            writer.writerow([
                item.emergency,
                item.country_name,
                item.iso3,
                item.admin_level_1,
                item.region,
                item.income_group,
                item.fragility_index_fund_for_peace,
                item.population_size,
                item.indicator_id,
                item.subvariable,
                item.indicator_name,
                item.thematic,
                item.thematic_description,
                item.topic,
                item.topic_description,
                item.indicator_description,
                item.type,
                item.indicator_value,
                item.error_margin,
                item.indicator_month,
                item.category,
            ])
        return response


class ExportCountryContextualDataView(ListAPIView):

    filterset_class = ContextualDataFilter
    queryset = ContextualData.objects.all()

    def get(self, request, format=None):
        """
        Export country contextual data
        """

        validate_export_params_together(self.request.query_params)
        filterset = ContextualDataFilter(
            data=self.request.query_params,
            queryset=self.get_queryset(),
        )
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="country-contextual-data.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow([
            'iso3',
            'context_date',
            'context_indicator_id',
            'context_indicator_value',
            'context_comment',
            'insert_date',
            'source',
            'context_subvariable',
            'emergency',
        ])
        for item in filterset.qs:
            writer.writerow([
                item.iso3,
                item.context_date,
                item.context_indicator_id,
                item.context_indicator_value,
                item.context_comment,
                item.insert_date,
                item.source,
                item.context_subvariable,
                item.emergency,
            ])
        return response
