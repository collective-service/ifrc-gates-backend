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
    DisaggregationType,
    ContextualDataType,
    RegionLevelType,
    ContextualDataWithMultipleEmergencyType,
    OverviewMapType,
    OverviewTableType,
    CombinedIndicatorType,
    IndicatorLatestStatsType,
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
    ContextIndicatorRegionLevelFilter,
    ContextIndicatorGlobalLevelFilter,
)
from .ordering import (
    RegionLevelOrder,
    GlobalLevelOrder,
    ContextualDataOrder,
    EpiDataGlobalOrder,
    CountryEmergencyProfileOrder,
    DataCountryLevelMostRecentOrder,
    DataGranularOrder
)
from .utils import (
    get_contextual_data_with_multiple_emergency,
    get_overview_map_data,
    get_overview_table_data,
    get_country_combined_indicators,
    get_region_combined_indicators,
    get_global_combined_indicators,
    get_indicator_stats_latest,
)
from utils import (
    get_redis_cache_data,
    set_redis_cache_data,
    get_values_list_from_dataclass,
)


async def get_country_profile_object(iso3):
    try:
        return await CountryProfile.objects.aget(iso3=iso3)
    except CountryProfile.DoesNotExist:
        return None


def get_outbreaks():
    return Outbreaks.objects.filter(active=True).order_by('outbreak')


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
        order=DataGranularOrder,
        pagination=True,
    )
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
        context_indicator_id: Optional[str] = None,
    ) -> List[ContextualDataWithMultipleEmergencyType]:
        return await get_contextual_data_with_multiple_emergency(
            iso3, emergency, context_indicator_id
        )

    @strawberry.field
    async def overview_map(
        self,
        emergency: Optional[str] = None,
        region: Optional[str] = None,
        indicator_id: Optional[str] = None,
    ) -> List[OverviewMapType]:
        prefix_key = 'overview-map'
        cached_data = get_redis_cache_data(prefix_key, emergency, region, indicator_id)
        if cached_data:
            return cached_data
        data = await get_overview_map_data(
            emergency,
            region,
            indicator_id,
        )
        set_redis_cache_data(prefix_key, emergency, region, indicator_id)
        return data

    @strawberry.field
    async def overview_table(
        self,
        emergency: Optional[str] = None,
        region: Optional[str] = None,
        indicator_id: Optional[str] = None,
    ) -> List[OverviewTableType]:
        prefix_key = 'overview-table'
        cached_data = get_redis_cache_data(prefix_key, emergency, region, indicator_id)
        if cached_data:
            return cached_data
        data = await get_overview_table_data(
            emergency,
            region,
            indicator_id,
        )
        set_redis_cache_data(prefix_key, emergency, region, indicator_id)
        return data

    @strawberry.field
    async def country_combined_indicators(
        filters: Optional[DataCountryLevelMostRecentFilter] = None,
    ) -> List[CombinedIndicatorType]:
        prefix_key = 'country_combined_indicators'
        filter_values = get_values_list_from_dataclass(filters)
        cached_data = get_redis_cache_data(prefix_key, *filter_values)
        if cached_data:
            return cached_data
        data = await get_country_combined_indicators(filters)
        set_redis_cache_data(prefix_key, *filter_values, value=data)
        return data

    @strawberry.field
    async def region_combined_indicators(
        filters: Optional[ContextIndicatorRegionLevelFilter] = None,
    ) -> List[CombinedIndicatorType]:
        prefix_key = 'region_combined_indicators'
        filter_values = get_values_list_from_dataclass(filters)
        cached_data = get_redis_cache_data(prefix_key, *filter_values)
        if not filters and cached_data:
            return cached_data
        data = await get_region_combined_indicators(filters)
        set_redis_cache_data(prefix_key, *filter_values, value=data)
        return data

    @strawberry.field
    async def global_combined_indicators(
        filters: Optional[ContextIndicatorGlobalLevelFilter] = None,
    ) -> List[CombinedIndicatorType]:
        prefix_key = 'global_combined_indicators'
        filter_values = get_values_list_from_dataclass(filters)
        cached_data = get_redis_cache_data(prefix_key, *filter_values)
        if not filters and cached_data:
            return cached_data
        data = await get_global_combined_indicators(filters)
        set_redis_cache_data(prefix_key, *filter_values, value=data)
        return data

    @strawberry.field
    async def overview_ranking(
        self,
        is_top: Optional[bool] = None,
        emergency: Optional[str] = None,
        region: Optional[str] = None,
        indicator_id: Optional[str] = None,
    ) -> List[IndicatorLatestStatsType]:
        prefix_key = 'stats-latest'
        cached_data = get_redis_cache_data(prefix_key, emergency, region, indicator_id)
        if cached_data:
            return cached_data
        data = await get_indicator_stats_latest(
            emergency,
            region,
            indicator_id,
            is_top
        )
        set_redis_cache_data(prefix_key, emergency, region, indicator_id)
        return data
