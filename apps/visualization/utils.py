import re
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from django.db.models import Max, F, OuterRef, Subquery
from django.db.models.functions import TruncMonth
from .models import (
    DataCountryLevel,
    DataCountryLevelMostRecent,
    CountryFilterOptions,
    Sources,
    RegionLevel,
    Countries,
    ContextualData,
    CountryEmergencyProfile,
)
from utils import get_async_list_from_queryset


@sync_to_async
def get_country_name(iso3):
    try:
        return Countries.objects.get(iso3=iso3).country_name
    except Countries.DoesNotExist:
        return None


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
            'indicator_value'
        ).distinct('category')
    else:
        return []

    return [
        GenderDisaggregationType(
            category=category,
            indicator_value=value
        ) for category, value in data
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
            'indicator_value'
        ).distinct('category')
    else:
        return []
    return [
        GenderDisaggregationType(
            category=category,
            indicator_value=value
        ) for category, value in data
    ]


@sync_to_async
def get_outbreaks(iso3):
    return list(
        CountryFilterOptions.objects.filter(iso3=iso3).distinct('emergency').values_list('emergency', flat=True)
    )


@sync_to_async
def get_indicator_value_regional(obj):
    return RegionLevel.objects.filter(
        indicator_id=obj.indicator_id
    ).order_by('-indicator_month').first().indicator_value_regional


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
        ) for indicator in indicators.distinct().values('indicator_id', 'indicator_description')
    ]


@sync_to_async
def get_subvariables(iso3, indicator_id):
    subvariables = CountryFilterOptions.objects.filter(
        iso3=iso3,
    ).distinct('subvariable')
    if indicator_id:
        subvariables = subvariables.filter(indicator_id=indicator_id)
    return list(
        subvariables.distinct('subvariable').values_list('subvariable', flat=True)
    )


@sync_to_async
def get_types():
    return list(
        DataCountryLevelMostRecent.objects.distinct('type').values_list('type', flat=True)
    )


def get_thematics(type):
    qs = DataCountryLevelMostRecent.objects.all()
    if type:
        qs = qs.filter(type=type)
    return get_async_list_from_queryset(
        qs.distinct('thematic').values_list('thematic', flat=True)
    )


def get_topics(thematic):
    qs = DataCountryLevelMostRecent.objects.all()
    if thematic:
        qs = qs.filter(thematic=thematic)
    return get_async_list_from_queryset(
        qs.distinct('topic').values_list('topic', flat=True)
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
    ).distinct('key_words').values_list('key_words', flat=True)
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
        ).distinct('indicator_id')
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

    def get_unique_countries_data(qs):
        # TODO: Improve this logic
        data_country_map = {}
        for item in qs:
            if data_country_map:
                if data_country_map.get(item['iso3'], None):
                    pass
                else:
                    data_country_map[item['iso3']] = item['indicator_value']
            else:
                data_country_map[item['iso3']] = item['indicator_value']
        return [
            OverviewMapType(
                iso3=iso3,
                indicator_value=indicator_value
            ) for iso3, indicator_value in data_country_map.items()
        ]

    qs = CountryEmergencyProfile.objects.filter(
        context_indicator_id='total_cases',
    ).values('iso3').annotate(
        max_indicator_month=Max('context_date'),
        indicator_value=F('context_indicator_value'),
    )

    if emergency and not (indicator_id or region):
        qs = CountryEmergencyProfile.objects.filter(
            emergency=emergency,
            context_indicator_id='total_cases',
        ).values('iso3').annotate(
            max_indicator_month=Max('context_date'),
            indicator_value=F('context_indicator_value'),
        )

    elif indicator_id or region or emergency:
        all_filters = {
            'region': region,
            'indicator_id': indicator_id,
            'emergency': emergency,
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}
        qs = DataCountryLevelMostRecent.objects.filter(**filters).values('iso3').annotate(
            max_indicator_month=Max('indicator_month'),
            indicator_value=F('indicator_value'),
        ).order_by('subvariable', '-max_indicator_month')

    return get_unique_countries_data(qs)


@sync_to_async
def get_overview_table_data(
    emergency,
    region,
    indicator_id,
):
    from .types import OverviewTableType, OverviewTableDataType

    def format_indicator_value(iso3, qs_map):
        # TODO: Find alternative for this
        twelve_month_data = qs_map.get(iso3)
        month_data_sorted_by_subvariable = {}
        for item in twelve_month_data:
            if month_data_sorted_by_subvariable:
                if month_data_sorted_by_subvariable.get(item['month'], None):
                    pass
                else:
                    month_data_sorted_by_subvariable[item['month']] = item['indicator_value']
            else:
                month_data_sorted_by_subvariable[item['month']] = item['indicator_value']
        return [
            OverviewTableDataType(
                month=month,
                indicator_value=indicator_value,
            ) for month, indicator_value in month_data_sorted_by_subvariable.items()
        ]

    if emergency and not (indicator_id or region):
        emergency_profile_qs = CountryEmergencyProfile.objects.filter(
            emergency=emergency,
            context_indicator_id='total_cases',
            context_date__lte=TruncMonth(datetime.today()),
            context_date__gte=TruncMonth(datetime.today() - timedelta(days=365)),
        ).annotate(
            month=Max(TruncMonth('context_date'))
        ).values('iso3', 'month').annotate(
            max_indicator_month=Max('context_date'),
            indicator_value=F('context_indicator_value'),
        )
        emergency_profile_qs_iso3_map = {}
        for item in emergency_profile_qs:
            if emergency_profile_qs_iso3_map.get(item['iso3']):
                emergency_profile_qs_iso3_map[item['iso3']].append(
                    {'month': item['month'], 'indicator_value': item['indicator_value']}
                )
            else:
                emergency_profile_qs_iso3_map[item['iso3']] = [
                    {'month': item['month'], 'indicator_value': item['indicator_value']}
                ]

        qs = emergency_profile_qs.values('iso3').annotate(
            max_indicator_month=Max('context_date'),
            indicator_value=F('context_indicator_value'),
        )

        return [
            OverviewTableType(
                iso3=item['iso3'],
                data=format_indicator_value(item['iso3'], emergency_profile_qs_iso3_map)
            ) for item in qs
        ]

    else:
        all_filters = {
            'region': region,
            'indicator_id': indicator_id,
            'emergency': emergency,
            'indicator_month__lte': TruncMonth(datetime.today()),
            'indicator_month__gte': TruncMonth(datetime.today() - timedelta(days=365)),
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}
        country_most_recent_qs = DataCountryLevelMostRecent.objects.filter(**filters).values(
            'iso3', 'indicator_month'
        ).annotate(
            month=Max('indicator_month'),
            indicator_value=F('indicator_value'),
        ).order_by('subvariable', '-month')
        country_most_recent_qs_iso3_map = {}
        for item in country_most_recent_qs:
            if country_most_recent_qs_iso3_map.get(item['iso3']):
                country_most_recent_qs_iso3_map[item['iso3']].append(
                    {'month': item['month'], 'indicator_value': item['indicator_value']}
                )
            else:
                country_most_recent_qs_iso3_map[item['iso3']] = [
                    {'month': item['month'], 'indicator_value': item['indicator_value']}
                ]

        qs = country_most_recent_qs.values('iso3').order_by('subvariable').annotate(
            max_indicator_month=Max('indicator_month'),
        )
        return [
            OverviewTableType(
                iso3=item['iso3'],
                data=format_indicator_value(item['iso3'], country_most_recent_qs_iso3_map)
            ) for item in qs
        ]
