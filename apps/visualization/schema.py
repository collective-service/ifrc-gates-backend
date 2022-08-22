import strawberry
from .models import CountryProfile
from .types import (
    CountryProfileType,
    CountryEmergencyProfileType,
    NarrativesType,
    CountryType,
    EpiDataType,
    DataCountryLevelMostRecentType,
    GlobalLevelType,
    EpiDataGlobalType,
    OutbreaksType,
)
from typing import List
from asgiref.sync import sync_to_async
from typing import Optional


@sync_to_async
def get_country_profile_object(iso3):
    try:
        return CountryProfile.objects.get(iso3=iso3)
    except CountryProfile.DoesNotExist:
        return None


@strawberry.type
class Query:
    country_profiles: List[CountryProfileType] = strawberry.django.field()
    country_emergency_profile: List[CountryEmergencyProfileType] = strawberry.django.field()
    naratives: List[NarrativesType] = strawberry.django.field()
    countries: List[CountryType] = strawberry.django.field()
    # NOTE : Needed for future
    # data_country_level: List[DataCountryLevelType] = strawberry.django.field()
    epi_data: List[EpiDataType] = strawberry.django.field()
    data_country_level_most_recent: List[DataCountryLevelMostRecentType] = strawberry.django.field()
    global_level: List[GlobalLevelType] = strawberry.django.field()

    # NOTE : Needed for future
    # data_country_level_quantiles: List[DataCountryLevelQuantilesType] = strawberry.django.field()
    # data_granular: List[DataGranularType] = strawberry.django.field()
    epi_data_global: List[EpiDataGlobalType] = strawberry.django.field()
    out_breaks: List[OutbreaksType] = strawberry.django.field()
    # region_level: List[RegionLevelType] = strawberry.django.field()

    @strawberry.field
    def country_profile(self, iso3: Optional[str] = None) -> CountryProfileType:
        return get_country_profile_object(iso3)
