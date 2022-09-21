import strawberry
from strawberry import auto
from apps.visualization.models import (
    RegionLevel,
    GlobalLevel,
    ContextualData,
    EpiDataGlobal,
    CountryEmergencyProfile,
    DataCountryLevelMostRecent,
)


@strawberry.django.ordering.order(RegionLevel)
class RegionLevelOrder:
    indicator_month: auto
    indicator_id: auto
    indicator_value_regional: auto


@strawberry.django.ordering.order(GlobalLevel)
class GlobalLevelOrder:
    indicator_month: auto
    indicator_value_global: auto


@strawberry.django.ordering.order(ContextualData)
class ContextualDataOrder:
    context_date: auto
    context_indicator_value: auto


@strawberry.django.ordering.order(EpiDataGlobal)
class EpiDataGlobalOrder:
    context_date: auto
    context_indicator_value: auto


@strawberry.django.ordering.order(CountryEmergencyProfile)
class CountryEmergencyProfileOrder:
    context_date: auto
    context_indicator_value: auto

@strawberry.django.ordering.order(DataCountryLevelMostRecent)
class DataCountryLevelMostRecentOrder:
    indicator_month: auto
    indicator_value: auto
