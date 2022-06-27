from django.db import models


class TCountryProfile(models.Model):
    iso3 = models.CharField(primary_key=True, max_length=3)
    population_size = models.BigIntegerField(blank=True, null=True)
    region = models.CharField(max_length=15, blank=True, null=True)
    internet_access = models.FloatField(blank=True, null=True)
    internet_access_comment = models.CharField(max_length=1000, blank=True, null=True)
    internet_access_source = models.CharField(max_length=100, blank=True, null=True)
    literacy_rate = models.FloatField(blank=True, null=True)
    literacy_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    literacy_rate_source = models.CharField(max_length=100, blank=True, null=True)
    wash_access_national = models.FloatField(blank=True, null=True)
    wash_access_national_comment = models.CharField(max_length=1000, blank=True, null=True)
    wash_access_national_source = models.CharField(max_length=100, blank=True, null=True)
    wash_access_rural = models.FloatField(blank=True, null=True)
    wash_access_rural_comment = models.CharField(max_length=1000, blank=True, null=True)
    wash_access_rural_source = models.CharField(max_length=100, blank=True, null=True)
    wash_access_urban = models.FloatField(blank=True, null=True)
    wash_access_urban_comment = models.CharField(max_length=1000, blank=True, null=True)
    wash_access_urban_source = models.CharField(max_length=100, blank=True, null=True)
    stringency = models.FloatField(blank=True, null=True)
    mask_policy = models.FloatField(blank=True, null=True)
    stay_at_home_requirements = models.FloatField(blank=True, null=True)
    medical_staff = models.FloatField(blank=True, null=True)
    medical_staff_comment = models.CharField(max_length=1000, blank=True, null=True)
    medical_staff_source = models.CharField(max_length=100, blank=True, null=True)
    covid_risk = models.FloatField(blank=True, null=True)
    covid_risk_comment = models.CharField(max_length=1000, blank=True, null=True)
    covid_risk_source = models.CharField(max_length=100, blank=True, null=True)
    economic_support_index = models.FloatField(blank=True, null=True)
    economic_support_index_comment = models.CharField(max_length=1000, blank=True, null=True)
    economic_support_index_source = models.CharField(max_length=100, blank=True, null=True)
    vaccination_policy = models.FloatField(blank=True, null=True)
    vaccination_policy_index_comment = models.CharField(max_length=1000, blank=True, null=True)
    vaccination_policy_source = models.CharField(max_length=100, blank=True, null=True)
    boosters_rate = models.FloatField(blank=True, null=True)
    boosters_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    boosters_rate_source = models.CharField(max_length=100, blank=True, null=True)
    new_cases = models.FloatField(blank=True, null=True)
    total_cases = models.FloatField(blank=True, null=True)
    new_deaths = models.FloatField(blank=True, null=True)
    total_deaths = models.FloatField(blank=True, null=True)
    total_doses = models.FloatField(blank=True, null=True)
    fully_vaccinated_rate = models.FloatField(blank=True, null=True)
    new_cases_per_million = models.FloatField(blank=True, null=True)
    new_deaths_per_million = models.FloatField(blank=True, null=True)
    vaccinated_rate = models.FloatField(blank=True, null=True)
    vaccine_approvals = models.CharField(max_length=1000, blank=True, null=True)
    vaccine_supply = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_country_profile'


class TDataCountryLevel(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    country_name = models.CharField(max_length=50)
    iso3 = models.CharField(max_length=3)
    admin_level_1 = models.CharField(max_length=100)
    region = models.CharField(max_length=15, blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    indicator_id = models.CharField(max_length=6)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    dimension = models.CharField(max_length=20, blank=True, null=True)
    variable = models.CharField(max_length=50, blank=True, null=True)
    subvariable = models.CharField(max_length=50)
    indicator_month = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    area = models.CharField(max_length=15)
    population_size = models.BigIntegerField(blank=True, null=True)
    interpolated = models.SmallIntegerField(blank=True, null=True)
    indicator_value = models.FloatField(blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_data_country_level'
        unique_together = (
            ('emergency', 'iso3', 'indicator_month', 'indicator_id', 'subvariable', 'category', 'admin_level_1'),
        )


class TDataCountryLevelMostRecent(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    country_name = models.CharField(max_length=50)
    iso3 = models.CharField(max_length=3)
    admin_level_1 = models.CharField(max_length=100)
    region = models.CharField(max_length=15, blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    indicator_id = models.CharField(max_length=6)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    dimension = models.CharField(max_length=20, blank=True, null=True)
    variable = models.CharField(max_length=50, blank=True, null=True)
    subvariable = models.CharField(max_length=50)
    indicator_month = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    area = models.CharField(max_length=15)
    population_size = models.BigIntegerField(blank=True, null=True)
    interpolated = models.SmallIntegerField(blank=True, null=True)
    indicator_value = models.FloatField(blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    organisations = models.CharField(max_length=1000, blank=True, null=True)
    indicator_value_prev = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_data_country_level_most_recent'
        unique_together = (
            ('emergency', 'iso3', 'indicator_id', 'subvariable', 'indicator_month', 'category'),
        )


class TDataCountryLevelQuantiles(models.Model):
    indicator_month = models.CharField(max_length=10)
    indicator_id = models.CharField(max_length=6)
    subvariable = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    region = models.CharField(primary_key=True, max_length=15)
    median = models.FloatField(blank=True, null=True)
    perc25 = models.FloatField(blank=True, null=True)
    perc75 = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    min = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_data_country_level_quantiles'
        unique_together = (('region', 'indicator_id', 'subvariable', 'indicator_month', 'category'),)


class TDataGranular(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    iso3 = models.CharField(max_length=3)
    admin_level_1 = models.CharField(max_length=100)
    indicator_id = models.CharField(max_length=6)
    subvariable = models.CharField(max_length=50)
    question = models.CharField(max_length=1000, blank=True, null=True)
    indicator_value = models.FloatField()
    nominator = models.BigIntegerField(blank=True, null=True)
    denominator = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6)
    age_group = models.CharField(max_length=10)
    age_info = models.CharField(max_length=20)
    target_group = models.CharField(max_length=40)
    area = models.CharField(max_length=15)
    indicator_date = models.DateField()
    indicator_matching = models.CharField(max_length=8)
    error_margin = models.FloatField(blank=True, null=True)
    representativeness = models.CharField(max_length=15)
    limitation = models.CharField(max_length=1000, blank=True, null=True)
    indicator_comment = models.CharField(max_length=1000, blank=True, null=True)
    source_id = models.CharField(max_length=5)
    interpolated = models.SmallIntegerField()
    insert_date = models.DateTimeField(blank=True, null=True)
    publish = models.SmallIntegerField()
    indicator_month = models.CharField(max_length=10)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    dimension = models.CharField(max_length=20, blank=True, null=True)
    variable = models.CharField(max_length=50, blank=True, null=True)
    indicator_type = models.CharField(max_length=20, blank=True, null=True)
    indicator_publish = models.CharField(max_length=1, blank=True, null=True)
    country_name = models.CharField(max_length=50)
    region = models.CharField(max_length=15, blank=True, null=True)
    display_in_tableau = models.CharField(max_length=1)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=250)
    details = models.TextField(blank=True, null=True)
    authors = models.CharField(max_length=1000, blank=True, null=True)
    methodology = models.CharField(max_length=250, blank=True, null=True)
    sample_size = models.CharField(max_length=250, blank=True, null=True)
    target_pop = models.CharField(max_length=500, blank=True, null=True)
    scale = models.CharField(max_length=25, blank=True, null=True)
    quality_check = models.CharField(max_length=50, blank=True, null=True)
    access_type = models.CharField(max_length=25, blank=True, null=True)
    source_comment = models.CharField(max_length=5000, blank=True, null=True)
    publication_channel = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    source_date = models.DateField(blank=True, null=True)
    key_words = models.CharField(max_length=250, blank=True, null=True)
    source_status = models.CharField(max_length=15, blank=True, null=True)
    frequency = models.CharField(max_length=15, blank=True, null=True)
    sample_type = models.CharField(max_length=25, blank=True, null=True)
    population_size = models.BigIntegerField(blank=True, null=True)
    category = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_data_granular'
        unique_together = (
            (
                'emergency', 'iso3', 'indicator_month', 'indicator_id', 'subvariable',
                'category', 'admin_level_1', 'area', 'source_id'
            ),
        )


class TEpiData(models.Model):
    iso3 = models.CharField(primary_key=True, max_length=3)
    context_date = models.DateField()
    new_cases = models.FloatField()
    new_cases_source = models.CharField(max_length=100, blank=True, null=True)
    total_cases = models.FloatField(blank=True, null=True)
    total_cases_source = models.CharField(max_length=100, blank=True, null=True)
    new_deaths = models.FloatField(blank=True, null=True)
    new_deaths_source = models.CharField(max_length=100, blank=True, null=True)
    total_deaths = models.FloatField(blank=True, null=True)
    total_deaths_source = models.CharField(max_length=100, blank=True, null=True)
    total_doses = models.FloatField(blank=True, null=True)
    total_doses_source = models.CharField(max_length=100, blank=True, null=True)
    fully_vaccinated_rate = models.FloatField(blank=True, null=True)
    fully_vaccinated_rate_source = models.CharField(max_length=100, blank=True, null=True)
    mask_policy = models.FloatField(blank=True, null=True)
    mask_policy_source = models.CharField(max_length=100, blank=True, null=True)
    stay_at_home_requirements = models.FloatField(blank=True, null=True)
    stay_at_home_requirements_source = models.CharField(max_length=100, blank=True, null=True)
    stringency = models.FloatField(blank=True, null=True)
    stringency_source = models.CharField(max_length=100, blank=True, null=True)
    new_cases_per_million = models.FloatField(blank=True, null=True)
    new_cases_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    new_deaths_per_million = models.FloatField(blank=True, null=True)
    new_deaths_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    economic_support_index = models.FloatField(blank=True, null=True)
    economic_support_index_source = models.CharField(max_length=100, blank=True, null=True)
    vaccination_policy = models.FloatField(blank=True, null=True)
    vaccination_policy_source = models.CharField(max_length=100, blank=True, null=True)
    public_information_campaigns = models.FloatField(blank=True, null=True)
    public_information_campaigns_source = models.CharField(max_length=100, blank=True, null=True)
    vaccinated_rate = models.FloatField(blank=True, null=True)
    vaccinated_rate_source = models.CharField(max_length=100, blank=True, null=True)
    boosters_rate = models.FloatField(blank=True, null=True)
    boosters_rate_source = models.CharField(max_length=100, blank=True, null=True)
    vaccine_supply = models.FloatField(blank=True, null=True)
    vaccine_supply_source = models.CharField(max_length=100, blank=True, null=True)
    hosp_patients = models.FloatField(blank=True, null=True)
    hosp_patients_source = models.CharField(max_length=100, blank=True, null=True)
    hosp_patients_per_million = models.FloatField(blank=True, null=True)
    hosp_patients_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    icu_patients = models.FloatField(blank=True, null=True)
    icu_patients_source = models.CharField(max_length=100, blank=True, null=True)
    icu_patients_per_million = models.FloatField(blank=True, null=True)
    icu_patients_per_million_source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_epi_data'
        unique_together = (('iso3', 'context_date'),)


class TGlobalLevel(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    region = models.CharField(max_length=6)
    indicator_id = models.CharField(max_length=6)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    dimension = models.CharField(max_length=20, blank=True, null=True)
    variable = models.CharField(max_length=50, blank=True, null=True)
    subvariable = models.CharField(max_length=50)
    indicator_month = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    indicator_value_global = models.FloatField(blank=True, null=True)
    population_coverage = models.FloatField(blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    std_dev = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_global_level'
        unique_together = (('emergency', 'region', 'indicator_month', 'indicator_id', 'subvariable', 'category'),)


class TRegionLevel(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    region = models.CharField(max_length=15)
    indicator_id = models.CharField(max_length=6)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    dimension = models.CharField(max_length=20, blank=True, null=True)
    variable = models.CharField(max_length=50, blank=True, null=True)
    subvariable = models.CharField(max_length=50)
    indicator_month = models.CharField(max_length=10)
    category = models.CharField(max_length=50)
    indicator_value_regional = models.FloatField(blank=True, null=True)
    population_coverage = models.FloatField(blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    std_dev = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_region_level'
        unique_together = (('emergency', 'region', 'indicator_month', 'indicator_id', 'subvariable', 'category'),)
