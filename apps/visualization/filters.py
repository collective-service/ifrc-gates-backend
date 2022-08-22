import strawberry
from django.db.models import Q
from typing import List
from .models import (
    CountryEmergencyProfile,
    Outbreaks,
    DataCountryLevel,
    DataCountryLevelMostRecent,
    RegionLevel,
    DataGranular
)


def disabled_outbreaks():
    return Outbreaks.objects.filter(
        active=False
    ).values_list('outbreak', flat=True)


@strawberry.django.filters.filter(CountryEmergencyProfile)
class CountryEmergencyProfileFilter:
    iso3: str
    emergencies: List[str] | None
    context_indicator_ids: List[str] | None

    def filter_emergencies(self, queryset):
        if not self.emergencies:
            return queryset
        return queryset.filter(
            Q(emergency__in=self.emergencies) &
            ~Q(emergency__in=disabled_outbreaks())
        )

    def filter_context_indicator_ids(self, queryset):
        if not self.context_indicator_ids:
            return queryset
        return queryset.filter(
            Q(context_indicator_id__in=self.context_indicator_ids) &
            ~Q(emergency__in=disabled_outbreaks())
        )


@strawberry.django.filters.filter(DataCountryLevel)
class DataCountryLevelFilter():
    iso3: str
    region: List[str] | None
    emergency: List[str] | None
    indicator_description: str
    indicator_name: str


@strawberry.django.filters.filter(DataCountryLevelMostRecent)
class DataCountryLevelMostRecentFilter():
    iso3: str
    region: str
    emergency: str
    indicator_description: str


@strawberry.django.filters.filter(RegionLevel)
class RegionLevelFilter():
    region: str
    emergency: str
    type: str
    category: str


@strawberry.django.filters.filter(DataGranular)
class DataGranularFilter():
    iso3: str
