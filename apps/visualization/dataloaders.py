from typing import List
from asgiref.sync import sync_to_async

from apps.visualization.models import (
    Countries,
    RegionLevel,
)


def country_name_load(keys: List[str]):
    return [Countries.objects.get(iso3=key).country_name for key in keys]


def indicator_value_regional_load(keys: List[int]):
    return [
        RegionLevel.objects.filter(
            indicator_id=key.indicator_id
        ).order_by('-indicator_month').first().indicator_value_regional for key in keys
    ]


load_country_name = sync_to_async(country_name_load)
load_indicator_value_regional = sync_to_async(indicator_value_regional_load)
