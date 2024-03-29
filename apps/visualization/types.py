# types.py
import strawberry
import datetime
import random
from typing import List, Optional
from strawberry import auto, ID
from strawberry.types import Info
from utils import (
    generate_id_from_unique_fields,
    generate_id_from_unique_field,
    generate_id_from_unique_non_model_fields,
)

from .utils import (
    get_outbreaks,
    get_country_indicators,
    get_gender_disaggregation_data,
    get_age_disaggregation_data,
    get_overview_indicators,
    get_subvariables,
    get_types,
    get_thematics,
    get_topics,
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
    ContextualData,
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

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


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
    population_comment: auto
    stringency_date: auto
    new_cases_region_share_date: auto
    new_cases_region_share_source: auto
    economic_support_index_date: auto
    readiness_date: auto
    readiness_source: auto
    risk_date: auto
    risk_source: auto
    vulnerability_date: auto
    vulnerability_source: auto
    response_date: auto
    response_source: auto
    internet_access_format: Optional[str]
    literacy_rate_format: Optional[str]
    wash_access_national_format: Optional[str]
    wash_access_rural_format: Optional[str]
    wash_access_urban_format: Optional[str]
    stringency_format: Optional[str]
    medical_staff_format: Optional[str]

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.django.type(CountryEmergencyProfile)
class CountryEmergencyProfileType:
    emergency: auto
    iso3: auto
    context_indicator_id: auto
    context_indicator_value: auto
    context_date: auto
    format: auto

    @strawberry.field
    def id(self) -> int:
        return generate_id_from_unique_fields(self)

    @strawberry.field
    def country_id(self) -> ID:
        return generate_id_from_unique_field(self.iso3)

    @strawberry.field
    async def country_name(self, info: Info) -> str:
        return await info.context["country_name_loader"].load(self.iso3)

    @strawberry.field
    async def population_size(self, info: Info) -> Optional[int]:
        return await info.context["population_size_loader"].load(self.iso3)


@strawberry.django.type(Narratives)
class NarrativesType:
    id: auto
    iso3: auto
    thematic: auto
    topic: auto
    indicator_id: auto
    narrative: auto
    insert_date: auto


@strawberry.django.type(DataCountryLevel)
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
    format: auto

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


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

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.django.type(DataCountryLevelMostRecent)
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
    topic_description: auto
    thematic_description: auto
    format: auto

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)

    @strawberry.field
    async def indicator_value_regional(self, info: Info) -> float:
        return await info.context["indicator_value_regional_loader"].load(self)


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
    topic_description: auto
    thematic_description: auto
    format: auto

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


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

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.django.type(DataGranular)
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
    format: auto

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.django.type(EpiDataGlobal)
class EpiDataGlobalType:
    region: auto
    emergency: auto
    context_date: auto
    context_indicator_id: auto
    context_indicator_value: auto
    most_recent: auto
    format: auto

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.django.type(Outbreaks)
class OutbreaksType:
    outbreak: auto
    active: auto


@strawberry.type
class CountryOutbreaksType:
    outbreak: str


@strawberry.django.type(RegionLevel)
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
    topic_description: auto
    thematic_description: auto
    format: auto

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.django.type(ContextualData)
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
    format: auto

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.type
class GenderDisaggregationType:
    category: Optional[str]
    indicator_value: Optional[float]
    format: Optional[str]

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_non_model_fields([self.category, self.indicator_value])


@strawberry.type
class AgeDisaggregationType:
    category: Optional[str]
    indicator_value: Optional[float]
    format: Optional[str]


@strawberry.type
class SourceType:
    title: Optional[str]
    source_comment: Optional[str]
    organisation: Optional[str]
    source_date: Optional[str]
    link: Optional[str]
    indicator_month: Optional[str]

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_non_model_fields(
            [self.title, self.source_comment, self.link, self.indicator_month, random.randint(1, 10000)]
        )


@strawberry.type
class DisaggregationType:
    @strawberry.field
    async def gender_disaggregation(
        self, iso3: str,
        indicator_id: Optional[str] = None,
        subvariable: Optional[str] = None
    ) -> List[GenderDisaggregationType]:

        return await get_gender_disaggregation_data(iso3, indicator_id, subvariable)

    @strawberry.field
    async def age_disaggregation(
        self,
        iso3: str,
        indicator_id: Optional[str] = None,
        subvariable: Optional[str] = None
    ) -> List[AgeDisaggregationType]:

        return await get_age_disaggregation_data(iso3, indicator_id, subvariable)


@strawberry.type
class CountryIndicatorType:
    indicator_id: Optional[str]
    indicator_description: Optional[str]
    type: Optional[str]
    emergencies: List[str]
    topic: str
    thematic: str


@strawberry.type
class OverviewIndicatorType:
    indicator_id: Optional[str]
    indicator_description: Optional[str]
    type: Optional[str]
    emergencies: List[str]
    topic: str
    thematic: str


@strawberry.type
class FilterOptionsType:

    @strawberry.field
    async def outbreaks(
        self,
        iso3: str,
    ) -> List[str]:
        return await get_outbreaks(iso3)

    @strawberry.field
    async def country_indicators(
        self,
        iso3: str,
        outbreak: Optional[str] = None,
        type: Optional[str] = None,
    ) -> List[CountryIndicatorType]:
        return await get_country_indicators(iso3, outbreak, type)

    @strawberry.field
    async def subvariables(
        self,
        indicator_id: str,
        iso3: Optional['str'] = None,
        emergency: Optional['str'] = None,
    ) -> List[str]:
        return await get_subvariables(indicator_id, iso3, emergency)

    @strawberry.field
    async def overview_indicators(
        self,
        out_break: Optional[str] = None,
        region: Optional[str] = None,
        type: Optional[str] = None,
        indicator_id: Optional[str] = None,
    ) -> List[OverviewIndicatorType]:

        return await get_overview_indicators(out_break, region, type, indicator_id)

    @strawberry.field
    async def types(self) -> List[str]:
        return await get_types()

    @strawberry.field
    async def thematics(self, type: Optional[str] = None) -> List[str]:
        return await get_thematics(type)

    @strawberry.field
    async def topics(self, thematics: Optional[List[str]] = None) -> List[str]:
        return await get_topics(thematics)


@strawberry.type
class ContexualDataMultipleType:
    iso3: str
    context_date: str
    context_indicator_value: Optional[float]
    context_indicator_id: Optional[str]
    format: Optional[str]

    @strawberry.field
    def id(self) -> ID:
        return generate_id_from_unique_fields(self)


@strawberry.type
class ContextualDataWithMultipleEmergencyType:
    emergency: str
    data: List[ContexualDataMultipleType]


@strawberry.type
class OverviewMapType:
    indicator_value: float
    iso3: str
    format: str
    emergency: str
    indicator_month: str
    subvariable: str

    @strawberry.field
    def country_id(self) -> ID:
        return generate_id_from_unique_field(self.iso3)


@strawberry.type
class OverviewTableDataType:
    month: str
    indicator_value: float
    format: str
    emergency: str
    subvariable: str


@strawberry.type
class OverviewTableType:
    iso3: str
    data: List[OverviewTableDataType]

    @strawberry.field
    def country_id(self) -> ID:
        return generate_id_from_unique_field(self.iso3)

    @strawberry.field
    async def country_name(self, info: Info) -> str:
        return await info.context["country_name_loader"].load(self.iso3)


@strawberry.type
class IndicatorType:
    emergency: str
    indicator_name: str
    indicator_id: Optional[str]
    indicator_description: Optional['str']
    indicator_value: Optional[float]
    indicator_value_regional: Optional[float]
    subvariable: Optional[str]
    region: Optional[str]
    format: Optional[str]
    indicator_month: Optional[str]


@strawberry.type
class CombinedIndicatorTopicType:
    topic_name: str
    topic_description: Optional[str]
    indicators: Optional[List[IndicatorType]]


@strawberry.type
class CombinedIndicatorType:
    thematic: str
    thematic_description: Optional[str]
    topics: Optional[List[CombinedIndicatorTopicType]]


@strawberry.type
class IndicatorLatestStatsType:
    indicator_value: float
    iso3: str
    format: str
    country_name: str
    subvariable: str
    emergency: str

    @strawberry.field
    def country_id(self) -> ID:
        return generate_id_from_unique_field(self.iso3)


@strawberry.type
class ExportMetaType:
    total_raw_data_count: int
    total_summary_count: int
    total_country_contextual_data_count: int
    max_page_limit: int


@strawberry.type
class SubvariableType:
    subvariable: str
    indicator_value: float
    indicator_description: Optional[str]
    format: Optional[str]
    indicator_month: datetime.date
    category: Optional[str]
