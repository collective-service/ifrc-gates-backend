import strawberry
from typing import List
from typing import Optional

from .models import (
    CountryProfile,
    Outbreaks,
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
    SourceType,
    DisaggregationType,
    ContextualDataType,
    RegionLevelType,
    ContextualDataWithMultipleEmergencyType,
    OverviewMapType,
    OverviewTableType,
)
from .filters import (
    CountryEmergencyProfileFilter,
    DataCountryLevelFilter,
    DataCountryLevelMostRecentFilter,
    RegionLevelFilter,
    DataGranularFilter,
    ContextualDataFilter,
    EpiDataGlobalFilter,
    GlobalLevelFilter,
    NarrativesFilter,
)
from .ordering import (
    RegionLevelOrder,
    GlobalLevelOrder,
    ContextualDataOrder,
    EpiDataGlobalOrder,
    CountryEmergencyProfileOrder,
    DataCountryLevelMostRecentOrder,
)
from .utils import (
    get_contextual_data_with_multiple_emergency,
    get_overview_map_data,
    get_overview_table_data,
    get_sources,
)


async def get_country_profile_object(iso3):
    try:
        return await CountryProfile.objects.aget(iso3=iso3)
    except CountryProfile.DoesNotExist:
        return None


def get_outbreaks():
    return Outbreaks.objects.filter(active=True)


@strawberry.type
class Query:
    country_profiles: List[CountryProfileType] = strawberry.django.field()
    country_emergency_profile: List[CountryEmergencyProfileType] = strawberry.django.field(
        filters=CountryEmergencyProfileFilter,
        order=CountryEmergencyProfileOrder,
        pagination=True,
    )
    naratives: List[NarrativesType] = strawberry.django.field(
        filters=NarrativesFilter
    )
    countries: List[CountryType] = strawberry.django.field()
    # NOTE : Needed for future
    epi_data: List[EpiDataType] = strawberry.django.field()
    data_country_level_most_recent: List[DataCountryLevelMostRecentType] = strawberry.django.field(
        filters=DataCountryLevelMostRecentFilter,
        order=DataCountryLevelMostRecentOrder,
        pagination=True,
    )
    global_level: List[GlobalLevelType] = strawberry.django.field(
        filters=GlobalLevelFilter,
        order=GlobalLevelOrder,
        pagination=True,
    )

    # NOTE : Needed for future
    # data_country_level_quantiles: List[DataCountryLevelQuantilesType] = strawberry.django.field()
    data_granular: List[DataGranularType] = strawberry.django.field(
        filters=DataGranularFilter,
        pagination=True,
    )
    # sources: List[SourcesType] = strawberry.django.field(
    #     filters=DataGranularFilter,
    #     pagination=True
    # )
    epi_data_global: List[EpiDataGlobalType] = strawberry.django.field(
        filters=EpiDataGlobalFilter,
        order=EpiDataGlobalOrder,
        pagination=True,
    )
    out_breaks: List[OutbreaksType] = strawberry.django.field(resolver=get_outbreaks)
    region_level: List[RegionLevelType] = strawberry.django.field(
        filters=RegionLevelFilter,
        order=RegionLevelOrder,
        pagination=True,
    )
    contextual_data: List[ContextualDataType] = strawberry.django.field(
        filters=ContextualDataFilter,
        order=ContextualDataOrder,
        pagination=True,
    )

    data_country_level: List[DataCountryLevelType] = strawberry.django.field(
        filters=DataCountryLevelFilter,
        pagination=True
    )

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
    async def contextualDataWithMultipleEmergency(
        self,
        iso3: Optional[str] = None,
        emergency: Optional[str] = None,
    ) -> List[ContextualDataWithMultipleEmergencyType]:
        return await get_contextual_data_with_multiple_emergency(
            iso3, emergency
        )

    @strawberry.field
    async def overview_map(
        self,
        emergency: Optional[str] = None,
        region: Optional[str] = None,
        indicator_id: Optional[str] = None,
    ) -> List[OverviewMapType]:
        return await get_overview_map_data(
            emergency,
            region,
            indicator_id,
        )

    @strawberry.field
    async def overview_table(
        self,
        emergency: Optional[str] = None,
        region: Optional[str] = None,
        indicator_id: Optional[str] = None,
    ) -> List[OverviewTableType]:
        return await get_overview_table_data(
            emergency,
            region,
            indicator_id,
        )

    @strawberry.field
    async def sources(
        self,
        iso3: Optional[str] = None,
        emergency: Optional[str] = None,
        indicator_name: Optional[str] = None,
        subvariable: Optional[str] = None,
    ) -> List[SourceType]:
        return await get_sources(
            iso3, emergency, indicator_name, subvariable
        )
