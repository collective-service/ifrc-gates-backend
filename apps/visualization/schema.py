import strawberry
from .types import CountryProfileType
from typing import List


@strawberry.type
class Query:
    country_profiles: List[CountryProfileType] = strawberry.django.field()
