import datetime
from django.utils import timezone

import strawberry
from typing import List
from asgiref.sync import sync_to_async
from typing import Optional

from .models import (
    CountryProfile,
    Outbreaks,
    ContextualData,
)
from .types import (
    CountryProfileType,
    CountryEmergencyProfileType,
    NarrativesType,
    CountryType,
    EpiDataType,
    DataCountryLevelType,
    DataCountryLevelMostRecentType,
    GlobalLevelType,
    EpiDataGlobalType,
    OutbreaksType,
    FilterOptionsType,
    DataGranularType,
    DisaggregationType,
    ContextualDataType
)
from apps.visualization.models import DataCountryLevel


@sync_to_async
def get_country_profile_object(iso3):
    try:
        return CountryProfile.objects.get(iso3=iso3)
    except CountryProfile.DoesNotExist:
        return None


def get_outbreaks():
    return Outbreaks.objects.filter(active=True)


@sync_to_async
def get_data_country_level(iso3, emergency, indicator, sub_indicator):

    date_before_twelve_month = timezone.now() - datetime.timedelta(12 * (365 / 12))
    all_filters = {
        'iso3': iso3,
        'emergency': emergency,
        'indicator_name': indicator,
        'subvariable': sub_indicator,
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
    return list(
        DataCountryLevel.objects.filter(
            **filters,
            indicator_month__gt=date_before_twelve_month
        ).order_by('-indicator_month')
    )


@sync_to_async
def get_contextual_data(iso3, emergency, context_indicator_id):

    date_before_twelve_month = timezone.now() - datetime.timedelta(12 * (365 / 12))
    all_filters = {
        'iso3': iso3,
        'emergency': emergency,
        'context_indicator_id': context_indicator_id
    }
    filters = {k: v for k, v in all_filters.items() if v is not None}
    return list(
        ContextualData.objects.filter(
            **filters,
            context_date__gt=date_before_twelve_month
        ).order_by('-context_date')
    )


@strawberry.type
class Query:
    country_profiles: List[CountryProfileType] = strawberry.django.field()
    country_emergency_profile: List[CountryEmergencyProfileType] = strawberry.django.field()
    naratives: List[NarrativesType] = strawberry.django.field()
    countries: List[CountryType] = strawberry.django.field()
    # NOTE : Needed for future
    epi_data: List[EpiDataType] = strawberry.django.field()
    data_country_level_most_recent: List[DataCountryLevelMostRecentType] = strawberry.django.field()
    global_level: List[GlobalLevelType] = strawberry.django.field()

    # NOTE : Needed for future
    # data_country_level_quantiles: List[DataCountryLevelQuantilesType] = strawberry.django.field()
    data_granular: List[DataGranularType] = strawberry.django.field()
    epi_data_global: List[EpiDataGlobalType] = strawberry.django.field()
    out_breaks: List[OutbreaksType] = strawberry.django.field(resolver=get_outbreaks)
    # region_level: List[RegionLevelType] = strawberry.django.field()
    contextual_data: List[ContextualDataType] = strawberry.django.field()

    @strawberry.field
    def country_profile(self, iso3: Optional[str] = None) -> CountryProfileType:
        return get_country_profile_object(iso3)

    @strawberry.field
    async def filter_options(self) -> FilterOptionsType:
        return FilterOptionsType

    @strawberry.field
    async def disaggregation(self) -> DisaggregationType:
        return DisaggregationType

    @strawberry.field
    def data_country_level(
        self,
        iso3: Optional[str],
        emergency: Optional[str] = None,
        indicator: Optional[str] = None,
        sub_indicator: Optional[str] = None
    ) -> List[DataCountryLevelType]:

        return get_data_country_level(iso3, emergency, indicator, sub_indicator)

    @strawberry.field
    def contextual_data(
        self,
        context_indicator_id: str,
        iso3: Optional[str],
        emergency: Optional[str] = None,
    ) -> List[ContextualDataType]:

        return get_contextual_data(iso3, emergency, context_indicator_id)
