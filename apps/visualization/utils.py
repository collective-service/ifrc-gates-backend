import re
from functools import reduce
from datetime import datetime, timedelta
from collections import defaultdict
from asgiref.sync import sync_to_async
from django.db.models import Max, F, FloatField, Q
from django.db.models.functions import TruncMonth
from django.db.models import OuterRef, Subquery
from strawberry_django.filters import apply as filter_apply

from .models import (
    DataCountryLevel,
    DataCountryLevelMostRecent,
    Sources,
    ContextualData,
    CountryEmergencyProfile,
    Countries,
    RegionLevel,
    GlobalLevel,
)
from apps.migrate_csv.models import CountryFilterOptions
from utils import get_async_list_from_queryset

COUNTRY_LEVEL = 'country_level'
REGIONAL_LEVEL = 'region_level'
GLOBAL_LEVEL = 'global_level'


@sync_to_async
def get_gender_disaggregation_data(iso3, indicator_id, subvariable):
    from .types import GenderDisaggregationType

    gender_category = ['Male', 'Female']
    all_filters = {
        'iso3': iso3,
        'indicator_id': indicator_id,
        'subvariable': subvariable
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
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

    all_filters = {
        'iso3': iso3,
        'indicator_id': indicator_id,
        'subvariable': subvariable
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
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
        CountryFilterOptions.objects.filter(
            iso3=iso3,
        ).distinct(
            'emergency'
        ).order_by('emergency').values_list('emergency', flat=True)
    )


@sync_to_async
def get_country_indicators(iso3, outbreak):
    from .types import CountryIndicatorType
    indicators = CountryFilterOptions.objects.filter(
        iso3=iso3,
    )
    if outbreak:
        indicators = indicators.filter(emergency=outbreak)
    return [
        CountryIndicatorType(
            indicator_id=indicator['indicator_id'],
            indicator_description=indicator['indicator_description'],
        ) for indicator in indicators.distinct().values('indicator_id', 'indicator_description').order_by('indicator_description')
    ]


@sync_to_async
def get_subvariables(iso3, indicator_id):
    subvariables = CountryFilterOptions.objects.filter(
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


async def clean_keywords(keywords_qs):
    data = set()
    async for keyword in keywords_qs:
        splited_keywords = re.split(";|,|\|", keyword.strip()) # noqa W605
        cleaned_keywords = [keyword.strip().capitalize() for keyword in filter(None, splited_keywords)]
        data.update(set(cleaned_keywords))
    return list(data)


def get_keywords():
    qs = Sources.objects.filter(
        key_words__isnull=False
    ).distinct('key_words').values_list('key_words', flat=True).order_by('key_words')
    return clean_keywords(qs)


@sync_to_async
def get_overview_indicators(out_break, region):
    from .types import OverviewIndicatorType

    all_filters = {
        'emergency': out_break,
        'region': region
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}

    options = list(
        DataCountryLevel.objects.filter(
            **filters,
        ).exclude(
            indicator_name=None
        ).values_list(
            'indicator_id',
            'indicator_description',
        ).distinct().order_by('indicator_description')
    )
    return [
        OverviewIndicatorType(
            indicator_id=name,
            indicator_description=description,
        ) for name, description in options
    ]


@sync_to_async
def get_contextual_data_with_multiple_emergency(
    iso3,
    emergency
):
    from .types import ContextualDataWithMultipleEmergencyType
    all_filters = {
        'iso3': iso3,
        'context_indicator_id': 'total_cases',
        'emergency': emergency,
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
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


@sync_to_async
def get_overview_map_data(
    emergency,
    region,
    indicator_id,
):
    from .types import OverviewMapType

    existing_iso3 = Countries.objects.values_list('iso3', flat=True)

    def get_unique_countries_data(qs):
        # TODO: Improve this logic
        data_country_map = {}
        for item in qs:
            if data_country_map:
                if data_country_map.get(item['iso3'], None):
                    pass
                else:
                    data_country_map[item['iso3']] = item
            else:
                data_country_map[item['iso3']] = item

        return [
            OverviewMapType(
                iso3=iso3,
                indicator_value=map_data['indicator_value'],
                format=map_data['format'],
            ) for iso3, map_data in data_country_map.items()
        ]

    if indicator_id or region or emergency:
        all_filters = {
            'region': region,
            'indicator_id': indicator_id,
            'emergency': emergency,
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}
        qs = DataCountryLevelMostRecent.objects.filter(
            **filters,
            iso3__in=existing_iso3,
        ).values('iso3').annotate(
            max_indicator_month=Max('indicator_month'),
            indicator_value=F('indicator_value'),
            format=F('format'),
        ).order_by('subvariable', '-max_indicator_month')

    else:
        all_filters = {
            'emergency': emergency,
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}
        qs = CountryEmergencyProfile.objects.filter(
            **filters,
            iso3__in=existing_iso3,
            context_indicator_id='new_cases_per_million',
        ).values('iso3').annotate(
            max_indicator_month=Max('context_date'),
            indicator_value=F('context_indicator_value'),
            format=F('format'),
        )
    return get_unique_countries_data(qs)


@sync_to_async
def get_overview_table_data(
    emergency,
    region,
    indicator_id,
):
    from .types import OverviewTableType, OverviewTableDataType

    existing_iso3 = Countries.objects.values_list('iso3', flat=True)

    def format_table_data(data):
        return {
            'month': data['month'],
            'indicator_value': data['indicator_value'],
            'format': data['format'],
        }

    def format_indicator_value(iso3, qs_map):

        # TODO: Find alternative for this
        twelve_month_data = qs_map.get(iso3)
        month_data_sorted_by_subvariable = {}
        for item in twelve_month_data:
            if month_data_sorted_by_subvariable:
                if month_data_sorted_by_subvariable.get(item['month'], None):
                    pass
                else:
                    month_data_sorted_by_subvariable[item['month']] = item
            else:
                month_data_sorted_by_subvariable[item['month']] = item
        return [
            OverviewTableDataType(
                month=month,
                indicator_value=table_data['indicator_value'],
                format=table_data['format'],
            ) for month, table_data in month_data_sorted_by_subvariable.items()
        ]

    if region or indicator_id:
        all_filters = {
            'region': region,
            'indicator_id': indicator_id,
            'emergency': emergency,
            'indicator_month__lte': TruncMonth(datetime.today()),
            'indicator_month__gte': TruncMonth(datetime.today() - timedelta(days=365)),
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}

        country_most_recent_qs = DataCountryLevelMostRecent.objects.filter(
            **filters,
            iso3__in=existing_iso3,
        ).values('iso3').annotate(
            indicator_value=Max('indicator_value'),
            month=F('indicator_month'),
            format=F('format'),
        ).order_by('subvariable')
        country_most_recent_qs_iso3_map = defaultdict()
        for item in country_most_recent_qs:
            country_most_recent_qs_iso3_map[item['iso3']] = [format_table_data(item)]
        unique_iso3 = set(list(country_most_recent_qs.values_list('iso3', flat=True)))
        return [
            OverviewTableType(
                iso3=iso3,
                data=format_indicator_value(iso3, country_most_recent_qs_iso3_map)
            ) for iso3 in unique_iso3
        ]
    else:
        all_filters = {
            'emergency': emergency,
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}
        emergency_profile_qs = CountryEmergencyProfile.objects.filter(
            iso3__in=existing_iso3,
            **filters,
            context_indicator_id='new_cases_per_million',
            context_date__lte=TruncMonth(datetime.today()),
            context_date__gte=TruncMonth(datetime.today() - timedelta(days=365)),
        ).values('iso3').annotate(
            max_indicator_month=Max('context_date'),
            indicator_value=F('context_indicator_value'),
            month=F('context_date'),
            format=F('format'),
        )
        emergency_profile_qs_iso3_map = defaultdict()
        for item in emergency_profile_qs:
            emergency_profile_qs_iso3_map[item['iso3']] = [format_table_data(item)]

        unique_iso3 = set(list(emergency_profile_qs.values_list('iso3', flat=True)))
        return [
            OverviewTableType(
                iso3=iso3,
                data=format_indicator_value(iso3, emergency_profile_qs_iso3_map)
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
                'indicator_value': Max('indicator_value'),
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
                'indicator_value': Max('indicator_value_regional'),
            }
        elif type == GLOBAL_LEVEL:
            return {
                'indicator_value': Max('indicator_value_global'),
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

    indicator_value_annotate_statement = get_indicator_value_annotate_statements(type)
    indicator_name_max_indicator_value_qs = await get_async_list_from_queryset(
        qs.values(
            'indicator_name', 'subvariable', 'indicator_id', 'indicator_description', 'format',
        ).annotate(
            max_indicator_month=F('indicator_month'),
            **indicator_value_annotate_statement,
        ).order_by('-max_indicator_month', 'subvariable')
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
                                'indicator_name': indicator_data['indicator_name'],
                                'indicator_value': indicator_data['indicator_value'],
                                'subvariable': indicator_data['subvariable'],
                                'indicator_id': indicator_data['indicator_id'],
                                'indicator_description': indicator_data['indicator_description'],
                                'format': indicator_data['format'],
                                'indicator_value_regional': indicator_data.get('indicator_value_regional', None),
                                'region': indicator_data.get('region', None),
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
    qs = DataCountryLevelMostRecent.objects.filter(category='Global')
    if filters:
        qs = filter_apply(filters, qs)
    return await process_combined_indicators(qs, type=COUNTRY_LEVEL)


async def get_region_combined_indicators(filters):
    qs = RegionLevel.objects.filter(category='Global')
    if filters:
        qs = filter_apply(filters, qs)
    return await process_combined_indicators(qs, type=REGIONAL_LEVEL)


async def get_global_combined_indicators(filters):
    qs = GlobalLevel.objects.filter(category='Global')
    if filters:
        qs = filter_apply(filters, qs)
    return await process_combined_indicators(qs, type=GLOBAL_LEVEL)
