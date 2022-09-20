import re
from asgiref.sync import sync_to_async
from django.db.models import Max, F
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


def get_overview_map_data(
    emergency,
    region,
    indicator_id,
):
    if emergency and not (indicator_id or region):
        return CountryEmergencyProfile.objects.filter(
            emergency=emergency,
            context_indicator_value='total_cases', 
        ).values('iso3').annotate(
            max_indicator_month=Max('context_indicator_month'),
            indicator_value=F('context_indicator_value'),
        )

    elif (indicator_id or region) and not emergency:
        all_filters = {
            'region': region,
            'indicator_id': indicator_id,
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}
        qs = DataCountryLevelMostRecent.objects.filter(**filters)
        return qs.values('iso3').annotate(
            max_indicator_month=Max('indicator_month'),
            indicator_value=F('indicator_value'),
        ).order_by('-max_indicator_month').distinct('iso3')
    return CountryEmergencyProfile.objects.filter(
        context_indicator_value='total_cases', 
    ).values('iso3').annotate(
        max_indicator_month=Max('context_indicator_month'),
        indicator_value=F('context_indicator_value'),
    )


def get_overview_table_data(
    emergency,
    region,
    indicator_id,
):
    if emergency and not (indicator_id or region):
        return CountryEmergencyProfile.objects.filter(
            emergency=emergency,
            context_indicator_value='total_cases', 
        ).values('iso3').annotate(
            max_indicator_month=Max('context_indicator_month'),
            indicator_value=F('context_indicator_value'),
        )

    elif (indicator_id or region) and not emergency:
        all_filters = {
            'region': region,
            'indicator_id': indicator_id,
        }
        filters = {k: v for k, v in all_filters.items() if v is not None}
        qs = DataCountryLevelMostRecent.objects.filter(**filters)
        return qs.values('iso3').annotate(
            max_indicator_month=Max('indicator_month'),
            indicator_value=F('indicator_value'),
        ).order_by('-max_indicator_month').distinct('iso3')
    return CountryEmergencyProfile.objects.filter(
        context_indicator_value='total_cases', 
    ).values('iso3').annotate(
        max_indicator_month=Max('context_indicator_month'),
        indicator_value=F('context_indicator_value'),
    )
