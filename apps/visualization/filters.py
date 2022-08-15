import strawberry
from django.db.models import Q
from typing import List
from strawberry import auto
from .models import CountryEmergencyProfile, Outbreaks


def disabled_outbreaks():
    return Outbreaks.objects.filter(
        active=False
    ).values_list('outbreak', flat=True)


@strawberry.django.filters.filter(CountryEmergencyProfile)
class CountryEmergencyProfileFilter:
    iso3: auto
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
