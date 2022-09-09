import strawberry
from django.db.models import Q
from typing import List
from .models import (
    CountryEmergencyProfile,
    Outbreaks,
    DataCountryLevel,
    DataCountryLevelMostRecent,
    RegionLevel,
    DataGranular,
    ContextualData,
    EpiDataGlobal
)


def disabled_outbreaks():
    return Outbreaks.objects.filter(
        active=False
    ).values_list('outbreak', flat=True)


@strawberry.django.filters.filter(CountryEmergencyProfile)
class CountryEmergencyProfileFilter:
    iso3: str
    emergency: str
    context_indicator_id: str

    def filter_emergency(self, queryset):
        if not self.emergency:
            return queryset
        return queryset.filter(
            Q(emergency=self.emergency) &
            ~Q(emergency__in=disabled_outbreaks())
        )

    def filter_context_indicator_id(self, queryset):
        if not self.context_indicator_id:
            return queryset
        return queryset.filter(
            Q(context_indicator_id=self.context_indicator_id) &
            ~Q(emergency__in=disabled_outbreaks())
        )


@strawberry.django.filters.filter(EpiDataGlobal)
class EpiDataGlobalFilter():
    region: str
    emergency: str
    context_indicator_id: str


@strawberry.django.filters.filter(DataCountryLevel)
class DataCountryLevelFilter():
    iso3: str
    emergency: str
    indicator_name: str
    subvariable: str
    category: str


@strawberry.django.filters.filter(DataCountryLevelMostRecent)
class DataCountryLevelMostRecentFilter():
    iso3: str
    emergency: str
    indicator_name: str
    subvariable: str
    topic: str
    thematic: str
    type: str
    source_ids: List[str]

    def filter_source_ids(self, queryset):
        if not self.source_ids:
            return queryset
        indicator_ids = DataGranular.objects.filter(
            source_id__in=self.source_ids
        ).values_list('indicator_id', flat=True)
        return queryset.filter(indicator_id__in=indicator_ids)


@strawberry.django.filters.filter(RegionLevel)
class RegionLevelFilter():
    region: str
    emergency: str
    type: str
    category: str


@strawberry.django.filters.filter(DataGranular)
class DataGranularFilter():
    iso3: str
    emergency: str
    indicator_name: str
    indicator_discription: str
    subvariable: str


@strawberry.django.filters.filter(ContextualData)
class ContextualDataFilter():
    iso3: str
    emergency: str
    context_indicator_id: str
