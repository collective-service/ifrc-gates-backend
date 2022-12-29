import strawberry
from django.db.models import Q
from typing import List
from typing import Optional
from strawberry_django.pagination import OffsetPaginationInput
from asgiref.sync import sync_to_async
from .models import (
    CountryProfile,
    Outbreaks,
    DataGranular,
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
    ExportMetaType,
    SubvariableType,
    SourceType,
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
    get_export_meta_data,
    get_region_level_subvariables,
    get_global_level_subvariables,
    clean_filters,
)
from utils import (
    get_redis_cache_data,
    set_redis_cache_data,
    get_values_list_from_dataclass,
    get_filtered_ordered_paginated_qs,
)


async def get_country_profile_object(iso3):
    try:
        return await CountryProfile.objects.aget(iso3=iso3)
    except CountryProfile.DoesNotExist:
        return None


@sync_to_async
def get_sources(iso3, emergency, indicator_id, indicator_name, indicator_description, subvariable, thematic, topic, type):
    filters = clean_filters({
        'iso3': iso3,
        'emergency': emergency,
        'indicator_id': indicator_id,
        'indicator_name': indicator_name,
        'indicator_description': indicator_description,
        'subvariable': subvariable,
        'thematic': thematic,
        'topic': topic,
        'type': type,
    })
    qs = DataGranular.objects.filter(
        ~Q(title="Interpolation", organisation="Interpolation"),
        **filters
    )
    latest_data_granular = qs.order_by('-indicator_month').first()
    if not latest_data_granular:
        return []
    data = qs.filter(indicator_month=latest_data_granular.indicator_month).distinct(
        'title',
        'source_comment',
        'organisation',
        'source_date',
        'link',
        'indicator_month',
    ).values(
        'title',
        'source_comment',
        'organisation',
        'source_date',
        'link',
        'indicator_month',
    )
    return [
        SourceType(
            title=item['title'],
            source_comment=item['source_comment'],
            organisation=item['organisation'],
            source_date=item['source_date'],
            link=item['link'],
            indicator_month=item['indicator_month'],
        ) for item in data
    ]


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
    narratives: List[NarrativesType] = strawberry.django.field(
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
    async def data_granular(
        self,
        filters: Optional[DataGranularFilter] = None,
        order: Optional[DataGranularOrder] = None,
        pagination: Optional[OffsetPaginationInput] = None,
    ) -> List[DataGranularType]:
        return await get_filtered_ordered_paginated_qs(
            DataGranular.objects.filter(
                ~Q(title="Interpolation", organisation="Interpolation")
            ),
            filters,
            order,
            pagination,
        )

    @strawberry.field
    async def sources(
        self,
        iso3: Optional[str] = None,
        emergency: Optional[str] = None,
        indicator_name: Optional[str] = None,
        indicator_id: Optional[str] = None,
        indicator_description: Optional[str] = None,
        subvariable: Optional[str] = None,
        thematic: Optional[str] = None,
        topic: Optional[str] = None,
        type: Optional[str] = None,
    ) -> List[SourceType]:
        return await get_sources(
            iso3, emergency, indicator_id, indicator_name,
            indicator_description, subvariable, thematic, topic, type
        )

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
        subvariable: Optional[str] = None,
    ) -> List[OverviewMapType]:
        prefix_key = 'overview-map'
        cached_data = get_redis_cache_data(prefix_key, emergency, region, indicator_id, subvariable)
        if cached_data:
            return cached_data
        data = await get_overview_map_data(
            emergency,
            region,
            indicator_id,
            subvariable,
        )
        set_redis_cache_data(prefix_key, emergency, region, indicator_id, subvariable, value=data)
        return data

    @strawberry.field
    async def overview_table(
        self,
        emergency: Optional[str] = None,
        region: Optional[str] = None,
        indicator_id: Optional[str] = None,
        subvariable: Optional[str] = None,
    ) -> List[OverviewTableType]:
        prefix_key = 'overview-table'
        cached_data = get_redis_cache_data(prefix_key, emergency, region, indicator_id, subvariable)
        if cached_data:
            return cached_data
        data = await get_overview_table_data(
            emergency,
            region,
            indicator_id,
            subvariable,
        )
        set_redis_cache_data(prefix_key, emergency, region, indicator_id, subvariable, value=data)
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
        subvariable: Optional[str] = None,
    ) -> List[IndicatorLatestStatsType]:
        prefix_key = 'stats-latest'
        cached_data = get_redis_cache_data(prefix_key, str(is_top), emergency, region, indicator_id, subvariable)
        if cached_data:
            return cached_data
        data = await get_indicator_stats_latest(
            emergency,
            region,
            indicator_id,
            subvariable,
            is_top,
        )
        set_redis_cache_data(prefix_key, emergency, region, indicator_id, subvariable, value=data)
        return data

    @strawberry.field
    async def export_meta(
        self,
        iso3: Optional[str] = None,
        indicator_id: Optional[str] = None,
    ) -> ExportMetaType:
        return await get_export_meta_data(iso3, indicator_id)

    @strawberry.field
    async def region_level_subvariables(
        self,
        region: Optional[str] = None,
        indicator_id: Optional[str] = None,
        emergency: Optional[str] = None,
    ) -> List[SubvariableType]:
        return await get_region_level_subvariables(region, indicator_id, emergency)

    @strawberry.field
    async def global_level_subvariables(
        self,
        indicator_id: Optional[str] = None,
        emergency: Optional[str] = None,
    ) -> List[SubvariableType]:
        return await get_global_level_subvariables(indicator_id, emergency)
