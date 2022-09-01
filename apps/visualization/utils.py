from asgiref.sync import sync_to_async

from .models import DataCountryLevel, DataCountryLevelMostRecent

from .filters import disabled_outbreaks


@sync_to_async
def get_gender_disaggregation_data(iso3, indicator_name, subvariable):
    from .types import GenderDisaggregationType

    gender_category = ['Male', 'Female']
    all_filters = {
        'iso3': iso3,
        'indicator_name': indicator_name,
        'subvariable': subvariable
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
    recent_data = DataCountryLevelMostRecent.objects.filter(**filters)
    if recent_data:
        datas = recent_data.filter(
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
        ) for category, value in datas
    ]


@sync_to_async
def get_age_disaggregation_data(iso3, indicator_name, subvariable):
    from .types import GenderDisaggregationType

    all_filters = {
        'iso3': iso3,
        'indicator_name': indicator_name,
        'subvariable': subvariable
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
    recent_data = DataCountryLevelMostRecent.objects.filter(**filters)
    if recent_data:
        datas = recent_data.filter(
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
        ) for category, value in datas
    ]


@sync_to_async
def get_indicators(iso3, out_break, indicator_name):
    from .types import IndicatorType

    if iso3:
        options = DataCountryLevel.objects.filter(
            iso3=iso3,
        ).exclude(emergency__in=disabled_outbreaks()).values_list(
            'emergency',
            'indicator_name',
            'indicator_description',
            'subvariable',
        ).distinct('emergency')

    elif iso3 and out_break:
        options = DataCountryLevel.objects.filter(
            iso3=iso3,
            emergency=out_break
        ).exclude(emergency__in=disabled_outbreaks()).values_list(
            'emergency',
            'indicator_name',
            'indicator_description',
            'subvariable',
        ).distinct('indicator_name')
    else:
        options = DataCountryLevel.objects.filter(
            iso3=iso3,
            emergency=out_break,
            indicator_name=indicator_name
        ).exclude(emergency__in=disabled_outbreaks()).values_list(
            'emergency',
            'indicator_name',
            'indicator_description',
            'subvariable',
        ).distinct('subvariable')
    return [
        IndicatorType(
            outbreak=out_break,
            indicator_name=indicator_name,
            indicator_description=indicator_description,
            subvariable=subvariable,
        ) for out_break, indicator_name, indicator_description, subvariable in options
    ]


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
            'indicator_name',
            'indicator_description',
        ).distinct('indicator_name')
    )
    return [
        OverviewIndicatorType(
            indicator_name=name,
            indicator_description=description,
        ) for name, description in options
    ]
