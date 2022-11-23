from functools import reduce
from datetime import datetime, timedelta
from collections import defaultdict

from asgiref.sync import sync_to_async
from django_cte import With
from django.db.models import (
    Max,
    F,
    FloatField,
    Q,
    Subquery,
    OuterRef,
)
from django.conf import settings
from django.db.models.functions import TruncMonth
from strawberry_django.filters import apply as filter_apply

from .models import (
    DataCountryLevel,
    DataCountryLevelMostRecent,
    ContextualData,
    Countries,
    RegionLevel,
    GlobalLevel,
    DataCountryLevelPublic,
    DataGranularPublic,
    DataCountryLevelPublicContext,
    Outbreaks,
)
from apps.migrate_csv.models import CachedCountryFilterOptions
from utils import get_async_list_from_queryset, clean_filters
from django.contrib.postgres.aggregates import ArrayAgg

COUNTRY_LEVEL = 'country_level'
REGIONAL_LEVEL = 'region_level'
GLOBAL_LEVEL = 'global_level'


def get_active_outbreaks_qs():
    # Use this function to query outbreaks in same schema
    return Outbreaks.objects.filter(active=True).values('outbreak')


def get_active_outbreaks_list():
    # Use this fuction to qyery outbreaks in different schema
    return list(
        Outbreaks.objects.filter(active=True).values_list('outbreak', flat=True)
    )


@sync_to_async
def get_gender_disaggregation_data(iso3, indicator_id, subvariable):
    from .types import GenderDisaggregationType

    gender_category = ['Male', 'Female']
    filters = clean_filters({
        'iso3': iso3,
        'indicator_id': indicator_id,
        'subvariable': subvariable
    })
    recent_data = DataCountryLevelMostRecent.objects.filter(**filters)
    if recent_data:
        data = recent_data.filter(
            indicator_month=recent_data.latest('indicator_month').indicator_month,
            category__in=gender_category
        ).values_list(
            'category',
            'indicator_value',
            'format',
        ).distinct('category')
    else:
        return []

    return [
        GenderDisaggregationType(
            category=category,
            indicator_value=value,
            format=format,
        ) for category, value, format in data
    ]


@sync_to_async
def get_age_disaggregation_data(iso3, indicator_id, subvariable):
    from .types import GenderDisaggregationType

    filters = clean_filters({
        'iso3': iso3,
        'indicator_id': indicator_id,
        'subvariable': subvariable
    })
    recent_data = DataCountryLevelMostRecent.objects.filter(**filters)
    if recent_data:
        data = recent_data.filter(
            category__regex=r'^((\d+)-(\d+)|(\d+\+))',
            indicator_month=recent_data.latest('indicator_month').indicator_month,
        ).values_list(
            'category',
            'indicator_value',
            'format',
        ).distinct('category')
    else:
        return []
    return [
        GenderDisaggregationType(
            category=category,
            indicator_value=value,
            format=format,
        ) for category, value, format in data
    ]


@sync_to_async
def get_outbreaks(iso3):
    return list(
        CachedCountryFilterOptions.objects.filter(
            iso3=iso3,
        ).distinct(
            'emergency'
        ).order_by('emergency').values_list('emergency', flat=True)
    )


@sync_to_async
def get_country_indicators(iso3, outbreak, type):
    from .types import CountryIndicatorType
    qs = CachedCountryFilterOptions.objects.filter(
        emergency__in=get_active_outbreaks_list()
    )
    filters = clean_filters({'iso3': iso3, 'emergency': outbreak, 'type': type})
    qs = qs.filter(
        **filters
    ).values(
        'indicator_id', 'indicator_description', 'type'
    ).annotate(
        emergencies=ArrayAgg('emergency', distinct=True)
    )

    return [
        CountryIndicatorType(
            indicator_id=indicator['indicator_id'],
            indicator_description=indicator['indicator_description'],
            type=indicator['type'],
            emergencies=indicator['emergencies']
        ) for indicator in qs
    ]


@sync_to_async
def get_subvariables(iso3, indicator_id):
    subvariables = CachedCountryFilterOptions.objects.filter(
        iso3=iso3,
    ).distinct('subvariable')
    if indicator_id:
        subvariables = subvariables.filter(indicator_id=indicator_id)
    return list(
        subvariables.distinct('subvariable').values_list('subvariable', flat=True).order_by('subvariable')
    )


@sync_to_async
def get_types():
    return list(
        DataCountryLevelMostRecent.objects.distinct('type').values_list('type', flat=True).order_by('type')
    )


def get_thematics(type):
    qs = DataCountryLevelMostRecent.objects.all()
    if type:
        qs = qs.filter(type=type)
    return get_async_list_from_queryset(
        qs.distinct('thematic').values_list('thematic', flat=True).order_by('thematic')
    )


def get_topics(thematic):
    qs = DataCountryLevelMostRecent.objects.all()
    if thematic:
        qs = qs.filter(thematic=thematic)
    return get_async_list_from_queryset(
        qs.distinct('topic').values_list('topic', flat=True).order_by('topic')
    )


@sync_to_async
def get_overview_indicators(out_break, region, type, indicator_id):
    from .types import OverviewIndicatorType

    filters = clean_filters({
        'emergency': out_break,
        'region': region,
        'type': type,
        'indicator_id': indicator_id,
    })
    options = list(
        DataCountryLevel.objects.filter(
            emergency__in=get_active_outbreaks_list(),
            **filters,
        ).exclude(
            indicator_name=None
        ).values(
            'indicator_id',
            'indicator_description',
            'type',
            'subvariable',
        ).annotate(
            emergencies=ArrayAgg('emergency', distinct=True)
        )
    )
    return [
        OverviewIndicatorType(
            indicator_id=item['indicator_id'],
            indicator_description=item['indicator_description'],
            type=item['type'],
            subvariable=item['subvariable'],
            emergencies=item['emergencies'],
        ) for item in options
    ]


@sync_to_async
def get_contextual_data_with_multiple_emergency(
    iso3,
    emergency,
    context_indicator_id,
):
    from .types import ContextualDataWithMultipleEmergencyType
    filters = clean_filters({
        'iso3': iso3,
        'emergency': emergency,
        'context_indicator_id': context_indicator_id,
    })
    contexual_data = ContextualData.objects.filter(
        **filters
    ).distinct('emergency').values('emergency')
    return [
        ContextualDataWithMultipleEmergencyType(
            emergency=emergency['emergency'],
            data=get_async_list_from_queryset(
                ContextualData.objects.filter(
                    **filters
                ).filter(
                    emergency=emergency['emergency']
                ).order_by('-context_date')[:12]
            )
        ) for emergency in contexual_data
    ]


def process_overview_data(filters, indicator_value_order='indicator_value'):
    countries_qs = Countries.objects.values('iso3')
    qs = DataCountryLevelMostRecent.objects.filter(
        **filters,
        iso3__in=countries_qs,
        category='Global',
    )
    if 'indicator_id' in filters:
        if 'subvariable' not in filters:
            qs = qs.filter(
                # NOTE: subvariable should not be empty, if empty contact cyrille
                subvariable=qs.order_by('subvariable').values('subvariable').distinct()[:1],
            )
    qs = qs.order_by(
        'iso3',
        '-indicator_month',
        'subvariable',
        indicator_value_order,
    ).distinct(
        'iso3',
    ).values(
        'iso3',
        'indicator_month',
        'subvariable',
        'indicator_value',
        'format',
        'country_name',
        'emergency',
    )
    qs_with = With(qs, name="qs")
    return (
        qs_with.queryset().with_cte(qs_with)
        .order_by(indicator_value_order)
    )


@sync_to_async
def get_overview_map_data(
    emergency,
    region,
    indicator_id,
    subvariable,
):
    from .types import OverviewMapType

    filters = clean_filters({
        'region': region,
        'indicator_id': indicator_id,
        'emergency': emergency,
        'subvariable': subvariable,
    })
    indicator_value_order = '-indicator_value'
    qs = process_overview_data(filters, indicator_value_order=indicator_value_order)
    return [
        OverviewMapType(
            iso3=item['iso3'],
            indicator_value=item['indicator_value'],
            format=item['format'],
            emergency=item['emergency'],
            indicator_month=item['indicator_month'],
            subvariable=item['subvariable'],
        ) for item in qs
    ]


@sync_to_async
def get_overview_table_data(
    emergency,
    region,
    indicator_id,
    subvariable,
):
    from .types import OverviewTableType, OverviewTableDataType

    countries_qs = Countries.objects.values_list('iso3', flat=True)

    def format_table_data(data):
        return OverviewTableDataType(
            month=data['indicator_month'],
            indicator_value=data['indicator_value'],
            format=data['format'],
            emergency=data['emergency'],
            subvariable=data['subvariable'],
        )

    filters = clean_filters({
        'region': region,
        'indicator_id': indicator_id,
        'emergency': emergency,
        'indicator_month__lte': TruncMonth(datetime.today()),
        'indicator_month__gte': TruncMonth(datetime.today() - timedelta(days=365)),
        'category': 'Global',
        'subvariable': subvariable,
    })

    qs = DataCountryLevel.objects.filter(
        **filters,
        iso3__in=countries_qs,
    )

    if 'subvariable' not in filters:
        qs = qs.filter(
            # NOTE: subvariable should not be empty, if empty contact to cyrille
            subvariable=qs.order_by('subvariable').values('subvariable').distinct()[:1],
        )
    country_most_recent_qs = qs.order_by(
        'iso3',
        '-indicator_month',
        'subvariable',
        '-indicator_value',
    ).distinct(
        'iso3',
        'indicator_month',
    ).values(
        'iso3',
        'indicator_month',
        'indicator_value',
        'format',
        'emergency',
        'subvariable',
    )
    country_most_recent_qs_iso3_map = {}
    for item in country_most_recent_qs:
        if country_most_recent_qs_iso3_map.get(item['iso3']):
            country_most_recent_qs_iso3_map[item['iso3']].append(format_table_data(item))
        else:
            country_most_recent_qs_iso3_map[item['iso3']] = [format_table_data(item)]
    unique_iso3 = set(list(country_most_recent_qs.values_list('iso3', flat=True)))
    return [
        OverviewTableType(
            iso3=iso3,
            data=country_most_recent_qs_iso3_map.get(iso3)
        ) for iso3 in unique_iso3
    ]


async def process_combined_indicators(qs, type):
    from .types import (
        CombinedIndicatorType,
        CombinedIndicatorTopicType,
        IndicatorType
    )

    def get_indicator_value_annotate_statements(type):
        '''
        Returns indicator values annotate statement to be annotated
        '''
        if type == COUNTRY_LEVEL:
            return {
                'indicator_value': Subquery(
                    DataCountryLevel.objects.filter(
                        iso3=OuterRef('iso3'),
                        indicator_id=OuterRef('indicator_id'),
                        subvariable=OuterRef('subvariable'),
                        region=OuterRef('region'),
                        emergency=OuterRef('emergency'),
                        category='Global',
                    ).order_by('-indicator_month', 'subvariable').values('indicator_value')[:1],
                    output_field=FloatField()
                ),
                'region_name': F('region'),
                'indicator_value_regional': Subquery(
                    RegionLevel.objects.filter(
                        indicator_id=OuterRef('indicator_id'),
                        subvariable=OuterRef('subvariable'),
                        region=OuterRef('region'),
                        category='Global',
                    ).order_by('-indicator_month', 'subvariable').values('indicator_value_regional')[:1],
                    output_field=FloatField()
                )
            }
        elif type == REGIONAL_LEVEL:
            return {
                'indicator_value': Subquery(
                    RegionLevel.objects.filter(
                        indicator_id=OuterRef('indicator_id'),
                        subvariable=OuterRef('subvariable'),
                        region=OuterRef('region'),
                        emergency=OuterRef('emergency'),
                        category='Global',
                    ).order_by('-indicator_month', 'subvariable').values('indicator_value_regional')[:1],
                    output_field=FloatField()
                )
            }
        elif type == GLOBAL_LEVEL:
            return {
                'indicator_value': Subquery(
                    GlobalLevel.objects.filter(
                        indicator_id=OuterRef('indicator_id'),
                        subvariable=OuterRef('subvariable'),
                        region=OuterRef('region'),
                        emergency=OuterRef('emergency'),
                        category='Global',
                    ).order_by('-indicator_month', 'subvariable').values('indicator_value_global')[:1],
                    output_field=FloatField()
                )
            }
        return {}

    thematics = await get_async_list_from_queryset(
        qs.values('thematic', 'thematic_description').distinct('thematic')
    )
    thematic_topic_qs = await get_async_list_from_queryset(
        qs.values(
            'thematic', 'topic', 'topic_description',
        ).distinct(
            'thematic', 'topic', 'topic_description',
        )
    )
    thematic_topic_map = defaultdict(list)
    for item in thematic_topic_qs:
        thematic_topic_map[item['thematic']].append({
            'topic': item['topic'],
            'topic_description': item['topic_description']
        })
    topic_indicator_name_qs = await get_async_list_from_queryset(
        qs.values('topic', 'indicator_name').distinct('topic', 'indicator_name')
    )
    topic_indicator_name_map = defaultdict(list)
    for item in topic_indicator_name_qs:
        topic_indicator_name_map[item['topic']].append(item['indicator_name'])

    indicator_value_annotate_statement = get_indicator_value_annotate_statements(type)

    indicators_with_max_month = await get_async_list_from_queryset(
        qs.values(
            'indicator_name', 'subvariable'
        ).annotate(
            max_indicator_month=Max('indicator_month'),
        ).order_by('-max_indicator_month', 'subvariable')
    )

    # TODO: Improve this
    indicator_filters = None
    if indicators_with_max_month:
        indicator_filters = reduce(
            lambda acc,
            item: acc | item,
            [
                Q(
                    indicator_name=value['indicator_name'],
                    indicator_month=value['max_indicator_month'],
                    subvariable=value['subvariable'],
                ) for value in indicators_with_max_month
            ]
        )
    if indicator_filters:
        qs = qs.filter(indicator_filters)

    if type == COUNTRY_LEVEL:
        indicator_name_max_indicator_value_qs = await get_async_list_from_queryset(
            qs.values(
                'iso3',
                'indicator_name',
                'subvariable',
                'indicator_id',
                'indicator_description',
                'format',
                'emergency',
            ).order_by('subvariable').annotate(
                max_indicator_month=Max('indicator_month'),
                **indicator_value_annotate_statement,
            )
        )
    else:
        indicator_name_max_indicator_value_qs = await get_async_list_from_queryset(
            qs.values(
                'indicator_name',
                'subvariable',
                'indicator_id',
                'indicator_description',
                'format',
                'emergency',
            ).order_by('subvariable').annotate(
                max_indicator_month=Max('indicator_month'),
                **indicator_value_annotate_statement,
            )
        )
    indicator_name_max_indicator_value_map = defaultdict(list)
    for item in indicator_name_max_indicator_value_qs:
        indicator_name_max_indicator_value_map[item['indicator_name']].append({
            'indicator_id': item['indicator_id'],
            'indicator_description': item['indicator_description'],
            'format': item['format'],
            'indicator_name': item['indicator_name'],
            'indicator_value': item['indicator_value'],
            'subvariable': item['subvariable'],
            'indicator_value_regional': item.get('indicator_value_regional', None),
            'region': item.get('region_name', None),
            'emergency': item['emergency'],
            'indicator_month': item['max_indicator_month'],
        })

    # Format data for dashboard
    data = []
    for thematic in thematics:
        data.append(
            {
                'thematic': thematic['thematic'],
                'thematic_description': thematic['thematic_description'],
                'topics': [
                    {
                        'topic_name': topic['topic'],
                        'topic_description': topic['topic_description'],
                        'indicators': [
                            {
                                'emergency': indicator_data['emergency'],
                                'indicator_name': indicator_data['indicator_name'],
                                'indicator_value': indicator_data['indicator_value'],
                                'subvariable': indicator_data['subvariable'],
                                'indicator_id': indicator_data['indicator_id'],
                                'indicator_description': indicator_data['indicator_description'],
                                'format': indicator_data['format'],
                                'indicator_value_regional': indicator_data.get('indicator_value_regional', None),
                                'region': indicator_data.get('region', None),
                                'indicator_month': indicator_data['indicator_month'],
                            } for indicator_name in topic_indicator_name_map.get(
                                topic['topic']
                            ) for indicator_data in indicator_name_max_indicator_value_map.get(
                                indicator_name
                            )
                        ]
                    } if topic else None for topic in thematic_topic_map.get(thematic['thematic'])
                ]
            }
        )
    return [
        CombinedIndicatorType(
            thematic=item['thematic'],
            thematic_description=item['thematic_description'],
            topics=[
                CombinedIndicatorTopicType(
                    topic_name=topic['topic_name'],
                    topic_description=topic['topic_description'],
                    indicators=[
                        IndicatorType(
                            **indicator
                        ) for indicator in topic['indicators']
                    ]
                ) for topic in item['topics']
            ],
        ) for item in data
    ]


async def get_country_combined_indicators(filters):
    qs = DataCountryLevelMostRecent.objects.filter(
        category='Global',
        emergency__in=get_active_outbreaks_qs(),
    )
    if filters:
        qs = filter_apply(filters, qs)
    return await process_combined_indicators(qs, type=COUNTRY_LEVEL)


async def get_region_combined_indicators(filters):
    qs = RegionLevel.objects.filter(
        category='Global',
        emergency__in=get_active_outbreaks_qs(),
    )
    if filters:
        qs = filter_apply(filters, qs)
    return await process_combined_indicators(qs, type=REGIONAL_LEVEL)


async def get_global_combined_indicators(filters):
    qs = GlobalLevel.objects.filter(
        category='Global',
        emergency__in=get_active_outbreaks_qs(),
    )
    if filters:
        qs = filter_apply(filters, qs)
    return await process_combined_indicators(qs, type=GLOBAL_LEVEL)


@sync_to_async
def get_indicator_stats_latest(
    emergency,
    region,
    indicator_id,
    subvariable,
    is_top=False,
):
    from .types import IndicatorLatestStatsType

    filters = clean_filters({
        'region': region,
        'emergency': emergency,
        'indicator_id': indicator_id,
        'indicator_value__gt': 0,
        'subvariable': subvariable,
    })

    indicator_value_order = 'indicator_value'
    if is_top:
        indicator_value_order = '-indicator_value'
    qs = process_overview_data(filters, indicator_value_order=indicator_value_order)
    return [
        IndicatorLatestStatsType(
            iso3=item['iso3'],
            indicator_value=item['indicator_value'],
            format=item['format'],
            country_name=item['country_name'],
            subvariable=item['subvariable'],
        ) for item in qs[:5]
    ]


@sync_to_async
def get_export_meta_data(iso3, indicator_id):
    from .types import ExportMetaType
    filters_map = {
        'iso3': iso3,
        'indicator_id': indicator_id,
    }
    filters = clean_filters(filters_map)
    return ExportMetaType(
        total_raw_data_count=DataGranularPublic.objects.filter(**filters).count(),
        total_summary_count=DataCountryLevelPublic.objects.filter(**filters).count(),
        total_country_contextual_data_count=DataCountryLevelPublicContext.objects.filter(**filters).count(),
        max_page_limit=settings.OPEN_API_MAX_EXPORT_PAGE_LIMIT,
    )
