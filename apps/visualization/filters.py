import strawberry
from datetime import timedelta
from django.db.models import (
    Q,
    Max,
    F,
    Subquery,
    OuterRef,
    CharField,
)
from functools import reduce
from .models import (
    CountryEmergencyProfile,
    Outbreaks,
    DataCountryLevel,
    DataCountryLevelMostRecent,
    RegionLevel,
    DataGranular,
    ContextualData,
    EpiDataGlobal,
    GlobalLevel,
    Countries,
    Narratives,
)
from strawberry import auto


def disabled_outbreaks():
    return Outbreaks.objects.filter(
        active=False
    ).values_list('outbreak', flat=True)


@strawberry.django.filters.filter(CountryEmergencyProfile)
class CountryEmergencyProfileFilter:
    iso3: str
    emergency: str
    context_indicator_id: str
    region: str

    def filter_emergency(self, queryset):
        if not self.emergency:
            return queryset
        return queryset.filter(
            Q(emergency=self.emergency) &
            ~Q(emergency__in=disabled_outbreaks())
        ).distinct()

    def filter_context_indicator_id(self, queryset):
        if not self.context_indicator_id:
            return queryset
        return queryset.filter(
            Q(context_indicator_id=self.context_indicator_id) &
            ~Q(emergency__in=disabled_outbreaks())
        ).distinct()

    def filter_region(self, queryset):
        if not self.region:
            return queryset
        return queryset.filter(
            iso3__in=Countries.objects.filter(region=self.region).values_list('iso3', flat=True)
        )


@strawberry.django.filters.filter(EpiDataGlobal)
class EpiDataGlobalFilter():
    region: str
    emergency: str
    context_indicator_id: str
    most_recent: auto
    is_global: bool
    is_twelve_month: bool
    is_regional_chart: bool

    def filter_is_global(self, queryset):
        if self.is_global:
            return queryset.filter(Q(region='Global'))
        return queryset.filter(~Q(region='Global'))

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            return queryset.order_by('-context_date')

    def filter_is_regional_chart(self, queryset):
        if self.is_regional_chart:
            most_recent_regional_data = queryset.filter(most_recent=True).exclude(region='Global').values('region').annotate(
                recent_context_date=Max('context_date'),
                max_context_indicator_value=Max('context_indicator_value')
            ).order_by('region')
            if most_recent_regional_data:
                filters = reduce(
                    lambda acc,
                    item: acc | item,
                    [
                        Q(
                            region=value['region'],
                            context_date=value['recent_context_date'],
                            context_indicator_value=value['max_context_indicator_value']
                        ) for value in most_recent_regional_data
                    ]
                )
                return queryset.filter(most_recent=True).filter(filters).annotate(
                    max_context_indicator_value=Max('context_indicator_value')
                ).filter(context_indicator_value=F('max_context_indicator_value'))
        return queryset


@strawberry.django.filters.filter(GlobalLevel)
class GlobalLevelFilter():
    emergency: str
    category: str
    indicator_id: str
    is_twelve_month: bool
    topic: str
    thematic: str
    type: str
    is_combined_indicators: bool
    is_most_recent: bool

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            greatest_subvariable_last_month = queryset.order_by(
                '-indicator_month', 'subvariable', '-indicator_value_global'
            ).first()
            if greatest_subvariable_last_month:
                return queryset.filter(
                    subvariable=greatest_subvariable_last_month.subvariable
                )
        return queryset

    def filter_is_combined_indicators(self, queryset):
        if self.is_combined_indicators:
            latest_subvariables = queryset.filter(category='Global').values('subvariable').annotate(
                latest_subvariable_month=Max('indicator_month'),
            )
            if latest_subvariables:
                filters = reduce(
                    lambda acc,
                    item: acc | item,
                    [
                        Q(
                            subvariable=value['subvariable'],
                            indicator_month=value['latest_subvariable_month'],
                        ) for value in latest_subvariables
                    ]
                )
                result = queryset.filter(filters).distinct('subvariable')
                return result

    def filter_is_most_recent(self, queryset):
        if self.is_most_recent:
            latest_emergency_data = queryset.filter(category='Global').values('emergency').annotate(
                latest_month=Max('indicator_month'),
                first_subvariable=Subquery(
                    GlobalLevel.objects.filter(
                        indicator_id=OuterRef('indicator_id'),
                        category='Global',
                    ).order_by('subvariable').values('subvariable')[:1],
                    output_field=CharField()
                )
            )
            if latest_emergency_data:
                filters = reduce(
                    lambda acc,
                    item: acc | item,
                    [
                        Q(
                            emergency=value['emergency'],
                            indicator_month=value['latest_month'],
                            subvariable=value['first_subvariable'],
                        ) for value in latest_emergency_data
                    ]
                )
                return queryset.filter(filters)
        return queryset


@strawberry.django.filters.filter(DataCountryLevel)
class DataCountryLevelFilter():
    iso3: str
    emergency: str
    indicator_name: str
    indicator_id: str
    subvariable: str
    category: str
    is_twelve_month: bool

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            max_indicator_date = queryset.aggregate(max_date=Max('indicator_month')).get('max_date')
            if max_indicator_date:
                queryset = queryset.filter(
                    indicator_month__gte=max_indicator_date - timedelta(days=365)
                ).order_by('-indicator_month')  # XXX: Avoid using ordering in the code.
        return queryset


@strawberry.django.filters.filter(DataCountryLevelMostRecent)
class DataCountryLevelMostRecentFilter():
    iso3: str
    emergency: str
    indicator_id: str
    subvariable: str
    topic: str
    thematic: str
    type: str
    region: str
    category: str


@strawberry.django.filters.filter(RegionLevel, lookups=True)
class RegionLevelFilter():
    region: str
    emergency: str
    category: str
    indicator_id: str
    is_twelve_month: bool
    subvariable: str
    topic: str
    thematic: str
    type: str
    is_regional_chart: bool
    is_combined_indicators: bool
    is_most_recent: bool

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            greatest_subvariable_last_month = queryset.order_by(
                '-indicator_month', 'subvariable', '-indicator_value_regional'
            ).first()
            return queryset.filter(
                subvariable=greatest_subvariable_last_month.subvariable
            )
        return queryset

    # NOTE :Create separate query in future.
    def filter_is_regional_chart(self, queryset):  # NOTE : Do not use order_by filter if this filter is used.
        subvariable = queryset.order_by('subvariable').first().subvariable
        if subvariable:
            data = queryset.filter(subvariable=subvariable).order_by(
                'region', '-indicator_month', 'subvariable', 'indicator_value_regional'
            ).distinct('region')
            return data
        return queryset

    def filter_is_combined_indicators(self, queryset):
        if self.is_combined_indicators:
            latest_subvariables = queryset.filter(category='Global').values('subvariable').annotate(
                latest_subvariable_month=Max('indicator_month'),
            )
            if latest_subvariables:
                filters = reduce(
                    lambda acc,
                    item: acc | item,
                    [
                        Q(
                            subvariable=value['subvariable'],
                            indicator_month=value['latest_subvariable_month'],
                        ) for value in latest_subvariables
                    ]
                )
                result = queryset.filter(filters).distinct('subvariable')
                return result
        return queryset

    def filter_is_most_recent(self, queryset):
        if self.is_most_recent:
            latest_emergency_data = queryset.filter(category='Global').values('region').annotate(
                latest_month=Max('indicator_month'),
                first_subvariable=Subquery(
                    RegionLevel.objects.filter(
                        indicator_id=OuterRef('indicator_id'),
                        category='Global',
                    ).order_by('subvariable').values('subvariable')[:1],
                    output_field=CharField()
                )
            )
            if latest_emergency_data:
                filters = reduce(
                    lambda acc,
                    item: acc | item,
                    [
                        Q(
                            region=value['region'],
                            indicator_month=value['latest_month'],
                            subvariable=value['first_subvariable'],
                        ) for value in latest_emergency_data
                    ]
                )
                return queryset.filter(filters)
        return queryset


@strawberry.django.filters.filter(DataGranular)
class DataGranularFilter():
    iso3: str
    emergency: str
    indicator_id: str
    indicator_name: str
    indicator_discription: str
    subvariable: str
    indicator_id: str
    is_distinct_sources: bool

    def filter_is_distinct_sources(self, queryset):
        # NOTE: This filter when selected shows data with distinct fields
        # title, organisation, source_date, link, source_comment
        if self.is_distinct_sources:
            return queryset.distinct(
                'title',
                'organisation',
                'source_date',
                'link',
                'source_comment'
            )
        return queryset


@strawberry.django.filters.filter(ContextualData)
class ContextualDataFilter():
    iso3: str
    emergency: str
    context_indicator_id: str
    is_twelve_month: bool

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            greatest_context_indicator_value = queryset.order_by(
                '-context_date'
            ).first()
            if greatest_context_indicator_value:
                return queryset.filter(
                    context_subvariable=greatest_context_indicator_value.context_subvariable
                )
            return queryset.none()
        return queryset


@strawberry.django.filters.filter(Narratives, lookups=True)
class NarrativesFilter():
    iso3: str
    indicator_id: str
    topic: str
    thematic: str

    def filter_indicator_id(self, queryset):
        if not self.indicator_id:
            return queryset
        topic = DataCountryLevel.objects.filter(
            indicator_id=self.indicator_id
        ).first().topic
        return queryset.filter(topic=topic)


@strawberry.django.filters.filter(RegionLevel, lookups=True)
class ContextIndicatorRegionLevelFilter():
    region: str
    emergency: str
    category: str
    indicator_id: str
    subvariable: str
    topic: str
    thematic: str
    type: str


@strawberry.django.filters.filter(GlobalLevel, lookups=True)
class ContextIndicatorGlobalLevelFilter():
    region: str
    emergency: str
    category: str
    indicator_id: str
    subvariable: str
    topic: str
    thematic: str
    type: str
