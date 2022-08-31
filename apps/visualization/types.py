# types.py
import strawberry
from typing import List, Optional
from strawberry import auto

from .utils import (
    get_indicators,
    get_gender_disaggregation_data,
    get_age_disaggregation_data,
    get_overview_indicators
)
from .models import (
    CountryProfile,
    CountryEmergencyProfile,
    Narratives,
    Countries,
    DataCountryLevel,
    EpiData,
    DataCountryLevelMostRecent,
    GlobalLevel,
    DataCountryLevelQuantiles,
    DataGranular,
    Outbreaks,
    EpiDataGlobal,
    RegionLevel,
    ContextualData
)
from .filters import (
    CountryEmergencyProfileFilter,
    DataCountryLevelFilter,
    DataCountryLevelMostRecentFilter,
    RegionLevelFilter,
    DataGranularFilter,
    ContextualDataFilter,
    EpiDataGlobalFilter
)


@strawberry.django.type(Countries)
class CountryType:
    iso3: auto
    iso2: auto
    country_name_full: auto
    country_name: auto
    region: auto
    flag_url: auto
    income_group: auto
    fragility_index_fund_for_peace: auto
    fragility_index_oecd: auto
    display_in_tableau: auto


@strawberry.django.type(CountryProfile)
class CountryProfileType:
    iso3: auto
    country_name: auto
    population_size: auto
    region: auto
    internet_access: auto
    internet_access_comment: auto
    internet_access_source: auto
    internet_access_region: auto
    literacy_rate: auto
    literacy_rate_comment: auto
    literacy_rate_source: auto
    literacy_rate_region: auto
    wash_access_national: auto
    wash_access_national_comment: auto
    wash_access_national_source: auto
    wash_access_national_region: auto
    wash_access_rural: auto
    wash_access_rural_comment: auto
    wash_access_rural_source: auto
    wash_access_urban: auto
    wash_access_urban_comment: auto
    wash_access_urban_source: auto
    stringency: auto
    stringency_region: auto
    mask_policy: auto
    stay_at_home_requirements: auto
    medical_staff: auto
    medical_staff_comment: auto
    medical_staff_source: auto
    medical_staff_region: auto
    covid_risk: auto
    covid_risk_comment: auto
    covid_risk_source: auto
    economic_support_index: auto
    economic_support_index_comment: auto
    economic_support_index_source: auto
    economic_support_index_region: auto
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


@strawberry.django.type(CountryEmergencyProfile, filters=CountryEmergencyProfileFilter)
class CountryEmergencyProfileType:
    emergency: auto
    iso3: auto
    context_indicator_id: auto
    context_indicator_value: auto
    context_date: auto


@strawberry.django.type(Narratives)
class NarrativesType:
    iso3: auto
    indicator_id: auto
    narrative: auto
    insert_date: auto


@strawberry.django.type(DataCountryLevel, filters=DataCountryLevelFilter)
class DataCountryLevelType():
    emergency: auto
    country_name: auto
    iso3: auto
    admin_level_1: auto
    region: auto
    income_group: auto
    fragility_index_fund_for_peace: auto
    indicator_id: auto
    subvariable: auto
    indicator_name: auto
    thematic: auto
    topic: auto
    indicator_description: auto
    type: auto
    indicator_month: auto
    category: auto
    population_size: auto
    interpolated: auto
    indicator_value: auto
    indicator_value_gradient: auto
    error_margin: auto
    display_in_tableau: auto


@strawberry.django.type(EpiData)
class EpiDataType:
    iso3: auto
    context_date: auto
    new_cases: auto
    new_cases_comment: auto
    new_cases_source: auto
    total_cases: auto
    total_cases_comment: auto
    total_cases_source: auto
    new_deaths: auto
    new_deaths_comment: auto
    new_deaths_source: auto
    total_deaths: auto
    total_deaths_comment: auto
    total_deaths_source: auto
    total_doses: auto
    total_doses_comment: auto
    total_doses_source: auto
    fully_vaccinated_rate: auto
    fully_vaccinated_rate_comment: auto
    fully_vaccinated_rate_source: auto
    mask_policy: auto
    mask_policy_comment: auto
    mask_policy_source: auto
    stay_at_home_requirements: auto
    stay_at_home_requirements_comment: auto
    stay_at_home_requirements_source: auto
    stringency: auto
    stringency_comment: auto
    stringency_source: auto
    new_cases_per_million: auto
    new_cases_per_million_comment: auto
    new_cases_per_million_source: auto
    new_deaths_per_million: auto
    new_deaths_per_million_comment: auto
    new_deaths_per_million_source: auto
    economic_support_index: auto
    economic_support_index_comment: auto
    economic_support_index_source: auto
    vaccination_policy: auto
    vaccination_policy_comment: auto
    vaccination_policy_source: auto
    public_information_campaigns: auto
    public_information_campaigns_comment: auto
    public_information_campaigns_source: auto
    vaccinated_rate: auto
    vaccinated_rate_comment: auto
    vaccinated_rate_source: auto
    boosters_rate: auto
    boosters_rate_comment: auto
    boosters_rate_source: auto
    vaccine_supply: auto
    vaccine_supply_source: auto
    hosp_patients: auto
    hosp_patients_comment: auto
    hosp_patients_source: auto
    hosp_patients_per_million: auto
    hosp_patients_per_million_comment: auto
    hosp_patients_per_million_source: auto
    icu_patients: auto
    icu_patients_comment: auto
    icu_patients_source: auto
    icu_patients_per_million: auto
    icu_patients_per_million_comment: auto
    icu_patients_per_million_source: auto


@strawberry.django.type(DataCountryLevelMostRecent, filters=DataCountryLevelMostRecentFilter)
class DataCountryLevelMostRecentType:
    emergency: auto
    country_name: auto
    iso3: auto
    admin_level_1: auto
    region: auto
    income_group: auto
    fragility_index_fund_for_peace: auto
    indicator_id: auto
    subvariable: auto
    indicator_name: auto
    thematic: auto
    topic: auto
    indicator_description: auto
    type: auto
    indicator_month: auto
    category: auto
    population_size: auto
    interpolated: auto
    indicator_value: auto
    indicator_value_gradient: auto
    error_margin: auto
    display_in_tableau: auto
    organisations: auto
    indicator_value_prev: auto


@strawberry.django.type(GlobalLevel)
class GlobalLevelType:
    emergency: auto
    region: auto
    indicator_id: auto
    subvariable: auto
    indicator_name: auto
    thematic: auto
    topic: auto
    indicator_description: auto
    type: auto
    indicator_month: auto
    category: auto
    indicator_value_global: auto
    population_coverage: auto
    error_margin: auto
    std_dev: auto


@strawberry.django.type(DataCountryLevelQuantiles)
class DataCountryLevelQuantilesType:
    emergency: auto
    indicator_month: auto
    indicator_id: auto
    subvariable: auto
    category: auto
    region: auto
    median: auto
    perc25: auto
    perc75: auto
    max: auto
    min: auto


@strawberry.django.type(DataGranular, filters=DataGranularFilter)
class DataGranularType:
    emergency: auto
    iso3: auto
    admin_level_1: auto
    indicator_id: auto
    subvariable: auto
    indicator_name: auto
    thematic: auto
    topic: auto
    indicator_description: auto
    type: auto
    direction: auto
    question: auto
    indicator_value: auto
    nominator: auto
    denominator: auto
    gender: auto
    age_group: auto
    age_info: auto
    target_group: auto
    indicator_date: auto
    indicator_matching: auto
    error_margin: auto
    representativeness: auto
    limitation: auto
    indicator_comment: auto
    source_id: auto
    interpolated: auto
    insert_date: auto
    publish: auto
    indicator_month: auto
    indicator_publish: auto
    country_name: auto
    region: auto
    display_in_tableau: auto
    income_group: auto
    fragility_index_fund_for_peace: auto
    organisation: auto
    title: auto
    details: auto
    authors: auto
    methodology: auto
    sample_size: auto
    target_pop: auto
    scale: auto
    quality_check: auto
    access_type: auto
    source_comment: auto
    publication_channel: auto
    link: auto
    source_date: auto
    key_words: auto
    source_status: auto
    frequency: auto
    sample_type: auto
    population_size: auto
    category: auto


@strawberry.django.type(EpiDataGlobal, filters=EpiDataGlobalFilter)
class EpiDataGlobalType:
    region: auto
    emergency: auto
    context_date: auto
    context_indicator_id: auto
    context_indicator_value: auto
    most_recent: auto


@strawberry.django.type(Outbreaks)
class OutbreaksType:
    outbreak: auto
    active: auto


@strawberry.type
class CountryOutbreaksType:
    outbreak: str


@strawberry.django.type(RegionLevel, filters=RegionLevelFilter)
class RegionLevelType:
    emergency: auto
    region: auto
    indicator_id: auto
    subvariable: auto
    indicator_name: auto
    thematic: auto
    topic: auto
    indicator_description: auto
    type: auto
    indicator_month: auto
    category: auto
    indicator_value_regional: auto
    population_coverage: auto
    error_margin: auto
    std_dev: auto


@strawberry.django.type(ContextualData, filters=ContextualDataFilter)
class ContextualDataType:
    iso3: auto
    context_date: auto
    context_indicator_id: auto
    context_indicator_value: auto
    context_comment: auto
    insert_date: auto
    source: auto
    context_subvariable: auto
    emergency: auto


@strawberry.type
class GenderDisaggregationType:
    category: str
    indicator_value: Optional[float]


@strawberry.type
class AgeDisaggregationType:
    category: str
    indicator_value: Optional[float]


@strawberry.type
class DisaggregationType:
    @strawberry.field
    async def gender_disaggregation(
        self, iso3: str,
        indicator_name: Optional[str] = None,
        subvariable: Optional[str] = None
    ) -> List[GenderDisaggregationType]:

        return await get_gender_disaggregation_data(iso3, indicator_name, subvariable)

    @strawberry.field
    async def age_disaggregation(
        self,
        iso3: str,
        indicator_name: Optional[str] = None,
        subvariable: Optional[str] = None
    ) -> List[AgeDisaggregationType]:

        return await get_age_disaggregation_data(iso3, indicator_name, subvariable)


@strawberry.django.type(DataCountryLevel)
class IndicatorType:
    outbreak: str
    indicator_name: auto
    indicator_description: auto
    subvariable: str


# @strawberry.django.type(DataCountryLevel)

@strawberry.type
class OverviewIndicatorType:
    indicator_name: Optional[str]
    indicator_description: Optional[str]


@strawberry.type
class FilterOptionsType:

    @strawberry.field
    async def indicators(
        self,
        iso3: Optional[str],
        out_break: Optional[str] = None,
        indicator_name: Optional[str] = None,
    ) -> List[IndicatorType]:

        return await get_indicators(iso3, out_break, indicator_name)

    @strawberry.field
    async def overview_indicators(
        self,
        out_break: Optional[str] = None,
        region: Optional[str] = None,
    ) -> List[OverviewIndicatorType]:

        return await get_overview_indicators(out_break, region)

