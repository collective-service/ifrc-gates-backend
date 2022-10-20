import strawberry
from typing import List
from typing import Optional
from strawberry_django.pagination import OffsetPaginationInput
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
)
from .utils import (
    get_contextual_data_with_multiple_emergency,
    get_overview_map_data,
    get_overview_table_data,
    get_country_combined_indicators,
    get_region_combined_indicators,
    get_global_combined_indicators,
)
from utils import (
    get_redis_cache_data,
    set_redis_cache_data,
    get_values_list_from_dataclass,
    get_filtered_ordered_paginated_qs,
    get_country_iso3_list,
)
from .models import (
    CountryEmergencyProfile,
    DataCountryLevelMostRecent,
    DataCountryLevel,
    DataGranular,
    ContextualData,
    EpiData,
    EpiDataGlobal,
    GlobalLevel,
    RegionLevel,
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
    naratives: List[NarrativesType] = strawberry.django.field(
        filters=NarrativesFilter
    )
    countries: List[CountryType] = strawberry.django.field()
    out_breaks: List[OutbreaksType] = strawberry.django.field(resolver=get_outbreaks)

    @strawberry.field
    def country_profile(self, iso3: Optional[str] = None) -> CountryProfileType:
        return get_country_profile_object(iso3)

    @strawberry.field
    async def country_emergency_profile(
        self,
        filters: Optional[CountryEmergencyProfileFilter] = None,
        order: Optional[CountryEmergencyProfileOrder] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[CountryEmergencyProfileType]:
        return await get_filtered_ordered_paginated_qs(
            CountryEmergencyProfile.objects.filter(
                iso3__in=get_country_iso3_list()
            ),
            filters,
            order,
            pagination,
        )

    @strawberry.field
    async def data_country_level_most_recent(
        self,
        filters: Optional[DataCountryLevelMostRecentFilter] = None,
        order: Optional[DataCountryLevelMostRecentOrder] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[DataCountryLevelMostRecentType]:
        return await get_filtered_ordered_paginated_qs(
            DataCountryLevelMostRecent.objects.filter(
                iso3__in=get_country_iso3_list()
            ),
            filters,
            order,
            pagination,
        )

    @strawberry.field
    async def data_country_level(
        self,
        filters: Optional[DataCountryLevelFilter] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[DataCountryLevelType]:
        return await get_filtered_ordered_paginated_qs(
            DataCountryLevel.objects.filter(
                iso3__in=get_country_iso3_list()
            ),
            filters,
            None,
            pagination,
        )

    @strawberry.field
    async def global_level(
        self,
        filters: Optional[GlobalLevelFilter] = None,
        order: Optional[GlobalLevelOrder] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[GlobalLevelType]:
        return await get_filtered_ordered_paginated_qs(
            GlobalLevel.objects.all(),
            filters,
            order,
            pagination,
        )

    @strawberry.field
    async def region_level(
        self,
        filters: Optional[RegionLevelFilter] = None,
        order: Optional[RegionLevelOrder] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[RegionLevelType]:
        return await get_filtered_ordered_paginated_qs(
            RegionLevel.objects.all(),
            filters,
            order,
            pagination,
        )

    @strawberry.field
    async def contextual_data(
        self,
        filters: Optional[ContextualDataFilter] = None,
        order: Optional[ContextualDataOrder] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[ContextualDataType]:
        return await get_filtered_ordered_paginated_qs(
            ContextualData.objects.filter(
                iso3__in=get_country_iso3_list()
            ),
            filters,
            order,
            pagination,
        )

    @strawberry.field
    async def data_granular(
        self,
        filters: Optional[DataGranularFilter] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[DataGranularType]:
        return await get_filtered_ordered_paginated_qs(
            DataGranular.objects.filter(
                iso3__in=get_country_iso3_list()
            ),
            filters,
            None,
            pagination,
        )

    @strawberry.field
    async def epi_data_global(
        self,
        filters: Optional[EpiDataGlobalFilter] = None,
        order: Optional[EpiDataGlobalOrder] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[EpiDataGlobalType]:
        return await get_filtered_ordered_paginated_qs(
            EpiDataGlobal.objects.all(),
            filters,
            order,
            pagination,
        )

    @strawberry.field
    async def epi_data(
        self,
    ) -> List[EpiDataType]:
        return await get_filtered_ordered_paginated_qs(
            EpiData.objects.filter(
                iso3__in=get_country_iso3_list()
            ),
            None,
            None,
            None,
        )

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
