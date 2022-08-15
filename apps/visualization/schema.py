import strawberry
from .models import CountryProfile
from .types import CountryProfileType, CountryEmergencyProfileType
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

    @strawberry.field
    def country_profile(self, iso3: Optional[str] = None) -> CountryProfileType:
        return get_country_profile_object(iso3)
