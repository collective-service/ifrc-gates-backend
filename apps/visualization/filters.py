import strawberry
from django.db.models import Q, Max, F
from typing import List
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
    Sources,
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

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            greatest_subvariable_last_month = queryset.order_by(
                '-indicator_month', '-indicator_value_global'
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
        return queryset


@strawberry.django.filters.filter(DataCountryLevel, lookups=True)
class DataCountryLevelFilter():
    iso3: str
    emergency: str
    indicator_name: str
    indicator_id: str
    subvariable: str
    category: str
    indicator_month: auto


@strawberry.django.filters.filter(DataCountryLevelMostRecent)
class DataCountryLevelMostRecentFilter():
    iso3: str
    emergency: str
    indicator_id: str
    subvariable: str
    topic: str
    thematic: str
    type: str
    keywords: List[str]

    def filter_keywords(self, queryset):
        if not self.keywords:
            return queryset

        keywords_filters = reduce(lambda acc, item: acc | item, [Q(key_words__icontains=value) for value in self.keywords])

        source_ids = Sources.objects.filter(keywords_filters).values_list('source_id', flat=True)
        indicator_ids = DataGranular.objects.filter(
            source_id__in=source_ids
        ).values_list('indicator_id', flat=True)
        return queryset.filter(indicator_id__in=indicator_ids)


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

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            greatest_subvariable_last_month = queryset.order_by(
                '-indicator_month', '-indicator_value_regional'
            ).first()
            return queryset.filter(
                subvariable=greatest_subvariable_last_month.subvariable
            )
        return queryset

    def filter_is_regional_chart(self, queryset):
        if self.is_regional_chart:
            regions_with_highest_indicator_month = queryset.values('region').annotate(
                latest_indicator_month=Max('indicator_month')
            ).order_by('region')
            if regions_with_highest_indicator_month:
                regions_with_highest_indicator_month_filter = reduce(
                    lambda acc, item: acc | item,
                    [
                        Q(
                            region=value['region'],
                            indicator_month=value['latest_indicator_month'],
                        ) for value in regions_with_highest_indicator_month
                    ]
                )
                regions_with_highest_indicator_month_highest_indicator_value_regional = queryset.filter(
                    regions_with_highest_indicator_month_filter
                ).values('region').annotate(
                    highest_indicator_value_regional=Max('indicator_value_regional'),
                    highest_indicator_month=Max('indicator_month'),
                )
                filters = reduce(
                    lambda acc,
                    item: acc | item,
                    [
                        Q(
                            region=value['region'],
                            indicator_value_regional=value['highest_indicator_value_regional'],
                            indicator_month=value['highest_indicator_month'],
                        ) for value in regions_with_highest_indicator_month_highest_indicator_value_regional
                    ]
                )
                return queryset.filter(filters)
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
    is_twelve_month: bool

    def filter_is_twelve_month(self, queryset):
        if self.is_twelve_month:
            greatest_context_indicator_value = queryset.order_by(
                '-context_date'
            ).first()
            return queryset.filter(
                context_subvariable=greatest_context_indicator_value.context_subvariable
            )
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
        print(topic)
        return queryset.filter(topic=topic)
