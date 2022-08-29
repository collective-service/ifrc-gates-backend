from asgiref.sync import sync_to_async

from .models import DataCountryLevel, DataCountryLevelMostRecent


@sync_to_async
def get_outbreaks(iso3):
    from .types import CountryOutbreaksType

    data = DataCountryLevelMostRecent.objects.filter(
        iso3=iso3
    ).values_list(
        'emergency',
    ).distinct('emergency')

    return [
        CountryOutbreaksType(
            outbreak=outbreak[0],
        ) for outbreak in data
    ]


@sync_to_async
def get_gender_disaggregation_data(iso3, indicator_name, subvariable):
    from .types import GenderDisaggregationType

    gender_category = ['Male', 'Female', 'Global']
    all_filters = {
        'iso3': iso3,
        'indicator_name': indicator_name,
        'subvariable': subvariable
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
    max_date = DataCountryLevelMostRecent.objects.filter(iso3=iso3).latest('indicator_month').indicator_month
    datas = DataCountryLevelMostRecent.objects.filter(
        **filters,
        indicator_month=max_date,
        category__in=gender_category
    ).values_list(
        'category',
        'indicator_value'
    ).distinct('category')

    return [
        GenderDisaggregationType(
            category=data[0],
            indicator_value=data[1]
        ) for data in datas
    ]


@sync_to_async
def get_age_disaggregation_data(iso3, indicator_name, subvariable):
    from .types import GenderDisaggregationType

    gender_category = ['Male', 'Female', 'Global']

    all_filters = {
        'iso3': iso3,
        'indicator_name': indicator_name,
        'subvariable': subvariable
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
    max_date = DataCountryLevelMostRecent.objects.filter(iso3=iso3).latest('indicator_month').indicator_month
    datas = DataCountryLevelMostRecent.objects.filter(
        **filters,
        indicator_month=max_date
    ).exclude(
        category__in=gender_category
    ).values_list(
        'category',
        'indicator_value'
    ).distinct('category')

    return [
        GenderDisaggregationType(
            category=data[0],
            indicator_value=data[1]
        ) for data in datas
    ]


@sync_to_async
def get_indicators(iso3, out_break, indicator_name):
    from .types import IndicatorType

    if iso3:
        options = DataCountryLevel.objects.filter(
            iso3=iso3,
        ).values_list(
            'emergency',
            'indicator_name',
            'indicator_description',
            'subvariable',
        ).distinct('emergency')

    elif iso3 and out_break:
        options = DataCountryLevel.objects.filter(
            iso3=iso3,
            emergency=out_break
        ).values_list(
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
        ).values_list(
            'emergency',
            'indicator_name',
            'indicator_description',
            'subvariable',
        ).distinct('subvariable')
    return [
        IndicatorType(
            outbreak=option[0],
            indicator_name=option[1],
            indicator_description=option[2],
            subvariable=option[3]
        ) for option in options
    ]
