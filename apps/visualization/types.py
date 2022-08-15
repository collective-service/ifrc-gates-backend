# types.py
import strawberry
from strawberry import auto
from .models import CountryProfile, CountryEmergencyProfile
from strawberry.types import Info
from typing import List
from .filters import CountryEmergencyProfileFilter


@strawberry.django.type(CountryProfile)
class CountryProfileType:
    iso3: auto
    country_name: auto
    population_size: auto
    region: auto
    internet_access: auto
    internet_access_comment: auto
    internet_access_source: auto
    literacy_rate: auto
    literacy_rate_comment: auto
    literacy_rate_source: auto
    wash_access_national: auto
    wash_access_national_comment: auto
    wash_access_national_source: auto
    wash_access_rural: auto
    wash_access_rural_comment: auto
    wash_access_rural_source: auto
    wash_access_urban: auto
    wash_access_urban_comment: auto
    wash_access_urban_source: auto
    stringency: auto
    mask_policy: auto
    stay_at_home_requirements: auto
    medical_staff: auto
    medical_staff_comment: auto
    medical_staff_source: auto
    covid_risk: auto
    covid_risk_comment: auto
    covid_risk_source: auto
    economic_support_index: auto
    economic_support_index_comment: auto
    economic_support_index_source: auto
    vaccination_policy: auto
    vaccination_policy_index_comment: auto
    vaccination_policy_source: auto
    boosters_rate: auto
    boosters_rate_comment: auto
    boosters_rate_source: auto
    new_cases: auto
    new_cases_region_share: auto
    total_cases: auto
    new_deaths: auto
    total_deaths: auto
    total_doses: auto
    fully_vaccinated_rate: auto
    new_cases_per_million: auto
    new_deaths_per_million: auto
    vaccinated_rate: auto
    vaccine_approvals: auto
    vaccine_supply: auto
    readiness: auto
    vulnerability: auto
    risk: auto
    response: auto


@strawberry.django.type(CountryProfile)
class CountryListType(CountryProfileType):
    pass


@strawberry.django.type(CountryEmergencyProfile, filters=CountryEmergencyProfileFilter)
class CountryEmergencyProfileType:
    emergency: auto
    iso3: auto
    context_indicator_id: auto
    context_indicator_value: auto
    context_date: auto
