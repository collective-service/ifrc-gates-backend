from asgiref.sync import sync_to_async

from .models import DataCountryLevelMostRecent


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
def get_indicators(iso3, indicator_name):
    from .types import IndicatorType

    if iso3 and indicator_name:
        data = DataCountryLevelMostRecent.objects.filter(
            iso3=iso3,
            indicator_name=indicator_name
        ).values_list(
            'indicator_name',
            'indicator_description',
            'subvariable',
        ).distinct('subvariable')
    else:
        data = DataCountryLevelMostRecent.objects.filter(
            iso3=iso3
        ).values_list(
            'indicator_name',
            'indicator_description',
            'subvariable',
        ).distinct('indicator_name')
    return [
        IndicatorType(
            indicator_name=indicator[0],
            indicator_description=indicator[1],
            subvariable=indicator[2]
        ) for indicator in data
    ]
