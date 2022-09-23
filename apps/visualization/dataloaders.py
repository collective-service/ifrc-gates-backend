from typing import List
from asgiref.sync import sync_to_async
from collections import defaultdict

from django.db.models import Max
from apps.visualization.models import (
    Countries,
    RegionLevel,
)


def country_name_load(keys: List[str]):
    countries = Countries.objects.filter(iso3__in=keys).values('iso3', 'country_name')
    _map = defaultdict(str)
    for country in countries:
        _map[country['iso3']] = country['country_name']
    return [_map[key] for key in keys]


def indicator_value_regional_load(keys: List[int]):
    indicator_id_list = [key.indicator_id for key in keys]
    indicator_value_regional = RegionLevel.objects.filter(
        indicator_id__in=indicator_id_list
    ).values(
        'indicator_id', 'indicator_value_regional'
    ).annotate(
        max_indicator_month=Max('indicator_month')
    ).order_by('-indicator_month')
    _map = defaultdict()
    for value in indicator_value_regional:
        _map[value['indicator_id']] = value['indicator_value_regional']
    return [_map[key] for key in indicator_id_list]


load_country_name = sync_to_async(country_name_load)
load_indicator_value_regional = sync_to_async(indicator_value_regional_load)
