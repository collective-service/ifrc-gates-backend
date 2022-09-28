from django.db import models


class Narratives(models.Model):
    id = models.AutoField(primary_key=True)
    iso3 = models.CharField(max_length=3)
    thematic = models.CharField(max_length=50, default='')
    topic = models.CharField(max_length=50, default='')
    indicator_id = models.CharField(max_length=6, default='')
    narrative = models.TextField()
    insert_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'narratives'
        unique_together = (
            ('iso3', 'thematic', 'topic', 'indicator_id'),
        )

    def __str__(self):
        return f'{self.id}-{self.insert_date}'


class Countries(models.Model):
    iso3 = models.CharField(primary_key=True, max_length=3)
    iso2 = models.CharField(max_length=2, blank=True, null=True)
    country_name_full = models.CharField(max_length=50, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=15, blank=True, null=True)
    flag_url = models.CharField(max_length=100, blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_oecd = models.CharField(max_length=50, blank=True, null=True)
    display_in_tableau = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_countries'
        unique_together = (
            ('iso3',)
        )


class ContextualData(models.Model):
    iso3 = models.CharField(max_length=3, primary_key=True)
    context_date = models.DateField()
    context_indicator_id = models.CharField(max_length=50)
    context_indicator_value = models.FloatField(blank=True, null=True)
    context_comment = models.CharField(max_length=1000, blank=True, null=True)
    insert_date = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    context_subvariable = models.CharField(max_length=100)
    emergency = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_contextual_data'
        unique_together = (
            (
                'iso3', 'context_date', 'emergency',
                'context_indicator_id', 'context_subvariable'
            ),
        )


class CountryEmergencyProfile(models.Model):
    emergency = models.CharField(max_length=50)
    iso3 = models.CharField(primary_key=True, max_length=3)
    context_indicator_id = models.CharField(max_length=255)
    context_indicator_value = models.FloatField(blank=True, null=True)
    context_date = models.DateField(blank=True, null=True)
    format = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_country_emergency_profile'
        unique_together = (('iso3', 'context_indicator_id', 'emergency'),)


class CountryProfile(models.Model):
    iso3 = models.CharField(primary_key=True, max_length=3)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    population_size = models.BigIntegerField(blank=True, null=True)
    region = models.CharField(max_length=15, blank=True, null=True)
    internet_access = models.FloatField(blank=True, null=True)
    internet_access_comment = models.CharField(max_length=1000, blank=True, null=True)
    internet_access_source = models.CharField(max_length=100, blank=True, null=True)
    internet_access_region = models.FloatField(blank=True, null=True)
    literacy_rate = models.FloatField(blank=True, null=True)
    literacy_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    literacy_rate_source = models.CharField(max_length=100, blank=True, null=True)
    literacy_rate_region = models.FloatField(blank=True, null=True)
    wash_access_national = models.FloatField(blank=True, null=True)
    wash_access_national_comment = models.CharField(max_length=1000, blank=True, null=True)
    wash_access_national_source = models.CharField(max_length=100, blank=True, null=True)
    wash_access_national_region = models.FloatField(blank=True, null=True)
    wash_access_rural = models.FloatField(blank=True, null=True)
    wash_access_rural_comment = models.CharField(max_length=1000, blank=True, null=True)
    wash_access_rural_source = models.CharField(max_length=100, blank=True, null=True)
    wash_access_urban = models.FloatField(blank=True, null=True)
    wash_access_urban_comment = models.CharField(max_length=1000, blank=True, null=True)
    wash_access_urban_source = models.CharField(max_length=100, blank=True, null=True)
    stringency = models.FloatField(blank=True, null=True)
    stringency_region = models.FloatField(blank=True, null=True)
    mask_policy = models.FloatField(blank=True, null=True)
    stay_at_home_requirements = models.FloatField(blank=True, null=True)
    medical_staff = models.FloatField(blank=True, null=True)
    medical_staff_comment = models.CharField(max_length=1000, blank=True, null=True)
    medical_staff_source = models.CharField(max_length=100, blank=True, null=True)
    medical_staff_region = models.FloatField(blank=True, null=True)
    covid_risk = models.FloatField(blank=True, null=True)
    covid_risk_comment = models.CharField(max_length=1000, blank=True, null=True)
    covid_risk_source = models.CharField(max_length=100, blank=True, null=True)
    economic_support_index = models.FloatField(blank=True, null=True)
    economic_support_index_comment = models.CharField(max_length=1000, blank=True, null=True)
    economic_support_index_source = models.CharField(max_length=100, blank=True, null=True)
    economic_support_index_region = models.FloatField(blank=True, null=True)
    vaccination_policy = models.FloatField(blank=True, null=True)
    vaccination_policy_index_comment = models.CharField(max_length=1000, blank=True, null=True)
    vaccination_policy_source = models.CharField(max_length=100, blank=True, null=True)
    boosters_rate = models.FloatField(blank=True, null=True)
    boosters_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    boosters_rate_source = models.CharField(max_length=100, blank=True, null=True)
    new_cases = models.FloatField(blank=True, null=True)
    new_cases_region_share = models.FloatField(blank=True, null=True)
    total_cases = models.FloatField(blank=True, null=True)
    new_deaths = models.FloatField(blank=True, null=True)
    total_deaths = models.FloatField(blank=True, null=True)
    total_doses = models.FloatField(blank=True, null=True)
    fully_vaccinated_rate = models.FloatField(blank=True, null=True)
    new_cases_per_million = models.FloatField(blank=True, null=True)
    new_deaths_per_million = models.FloatField(blank=True, null=True)
    vaccinated_rate = models.FloatField(blank=True, null=True)
    vaccine_approvals = models.TextField(blank=True, null=True)
    vaccine_supply = models.FloatField(blank=True, null=True)
    readiness = models.FloatField(blank=True, null=True)
    vulnerability = models.FloatField(blank=True, null=True)
    risk = models.FloatField(blank=True, null=True)
    response = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_country_profile'
        unique_together = (
            ('iso3',)
        )


class DataCountryLevel(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    iso3 = models.CharField(max_length=3)
    admin_level_1 = models.CharField(max_length=100)
    region = models.CharField(max_length=15, blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    indicator_id = models.CharField(max_length=6)
    subvariable = models.CharField(max_length=255)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    thematic = models.CharField(max_length=50, blank=True, null=True)
    thematic_description = models.CharField(max_length=250, blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    topic_description = models.CharField(max_length=250, blank=True, null=True)
    indicator_description = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    indicator_month = models.DateField()
    category = models.CharField(max_length=50)
    population_size = models.BigIntegerField(blank=True, null=True)
    interpolated = models.SmallIntegerField(blank=True, null=True)
    indicator_value = models.FloatField(blank=True, null=True)
    indicator_value_gradient = models.FloatField(blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    display_in_tableau = models.BooleanField(blank=True, null=True)
    format = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_data_country_level'
        unique_together = (
            (
                'emergency', 'iso3', 'indicator_month', 'indicator_id',
                'subvariable', 'category', 'admin_level_1'
            ),
        )


class DataCountryLevelMostRecent(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    iso3 = models.CharField(max_length=3)
    admin_level_1 = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=15, blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    indicator_id = models.CharField(max_length=6)
    subvariable = models.CharField(max_length=255)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    thematic = models.CharField(max_length=50, blank=True, null=True)
    thematic_description = models.CharField(max_length=250, blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    topic_description = models.CharField(max_length=250, blank=True, null=True)
    indicator_description = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    indicator_month = models.DateField()
    category = models.CharField(max_length=50)
    population_size = models.BigIntegerField(blank=True, null=True)
    interpolated = models.SmallIntegerField(blank=True, null=True)
    indicator_value = models.FloatField(blank=True, null=True)
    indicator_value_gradient = models.FloatField(blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    display_in_tableau = models.BooleanField(blank=True, null=True)
    organisations = models.TextField(blank=True, null=True)
    indicator_value_prev = models.TextField(blank=True, null=True)
    format = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_data_country_level_most_recent'
        unique_together = (
            (
                'emergency', 'iso3', 'indicator_id',
                'subvariable', 'indicator_month', 'category'
            ),
        )


class DataCountryLevelPublicContext(models.Model):
    iso3 = models.CharField(max_length=3)
    context_date = models.DateField()
    new_cases = models.FloatField(blank=True, null=True)
    new_cases_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_cases_source = models.CharField(max_length=100, blank=True, null=True)
    total_cases = models.FloatField(blank=True, null=True)
    total_cases_comment = models.CharField(max_length=1000, blank=True, null=True)
    total_cases_source = models.CharField(max_length=100, blank=True, null=True)
    new_deaths = models.FloatField(blank=True, null=True)
    new_deaths_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_deaths_source = models.CharField(max_length=100, blank=True, null=True)
    total_deaths = models.FloatField(blank=True, null=True)
    total_deaths_comment = models.CharField(max_length=1000, blank=True, null=True)
    total_deaths_source = models.CharField(max_length=100, blank=True, null=True)
    total_doses = models.FloatField(blank=True, null=True)
    total_doses_comment = models.CharField(max_length=1000, blank=True, null=True)
    total_doses_source = models.CharField(max_length=100, blank=True, null=True)
    fully_vaccinated_rate = models.FloatField(blank=True, null=True)
    fully_vaccinated_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    fully_vaccinated_rate_source = models.CharField(max_length=100, blank=True, null=True)
    mask_policy = models.FloatField(blank=True, null=True)
    mask_policy_comment = models.CharField(max_length=1000, blank=True, null=True)
    mask_policy_source = models.CharField(max_length=100, blank=True, null=True)
    stay_at_home_requirements = models.FloatField(blank=True, null=True)
    stay_at_home_requirements_comment = models.CharField(max_length=1000, blank=True, null=True)
    stay_at_home_requirements_source = models.CharField(max_length=100, blank=True, null=True)
    stringency = models.FloatField(blank=True, null=True)
    stringency_comment = models.CharField(max_length=1000, blank=True, null=True)
    stringency_source = models.CharField(max_length=100, blank=True, null=True)
    new_cases_per_million = models.FloatField(blank=True, null=True)
    new_cases_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_cases_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    new_deaths_per_million = models.FloatField(blank=True, null=True)
    new_deaths_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_deaths_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    economic_support_index = models.FloatField(blank=True, null=True)
    economic_support_index_comment = models.CharField(max_length=1000, blank=True, null=True)
    economic_support_index_source = models.CharField(max_length=100, blank=True, null=True)
    vaccination_policy = models.FloatField(blank=True, null=True)
    vaccination_policy_comment = models.CharField(max_length=1000, blank=True, null=True)
    vaccination_policy_source = models.CharField(max_length=100, blank=True, null=True)
    public_information_campaigns = models.FloatField(blank=True, null=True)
    public_information_campaigns_comment = models.CharField(max_length=1000, blank=True, null=True)
    public_information_campaigns_source = models.CharField(max_length=100, blank=True, null=True)
    vaccinated_rate = models.FloatField(blank=True, null=True)
    vaccinated_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    vaccinated_rate_source = models.CharField(max_length=100, blank=True, null=True)
    boosters_rate = models.FloatField(blank=True, null=True)
    boosters_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    boosters_rate_source = models.CharField(max_length=100, blank=True, null=True)
    vaccine_supply = models.FloatField(blank=True, null=True)
    vaccine_supply_source = models.CharField(max_length=100, blank=True, null=True)
    hosp_patients = models.FloatField(blank=True, null=True)
    hosp_patients_comment = models.CharField(max_length=1000, blank=True, null=True)
    hosp_patients_source = models.CharField(max_length=100, blank=True, null=True)
    hosp_patients_per_million = models.FloatField(blank=True, null=True)
    hosp_patients_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    hosp_patients_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    icu_patients = models.FloatField(blank=True, null=True)
    icu_patients_comment = models.CharField(max_length=1000, blank=True, null=True)
    icu_patients_source = models.CharField(max_length=100, blank=True, null=True)
    icu_patients_per_million = models.FloatField(blank=True, null=True)
    icu_patients_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    icu_patients_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    emergency = models.CharField(primary_key=True, max_length=50)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    admin_level_1 = models.CharField(max_length=100)
    region = models.CharField(max_length=15, blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    indicator_id = models.CharField(max_length=6)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    subvariable = models.CharField(max_length=255)
    thematic = models.CharField(max_length=50, blank=True, null=True)
    thematic_description = models.CharField(max_length=250, blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    topic_description = models.CharField(max_length=250, blank=True, null=True)
    category = models.CharField(max_length=50)
    population_size = models.BigIntegerField(blank=True, null=True)
    indicator_value = models.FloatField(blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_data_country_level_public_context'
        unique_together = (
            (
                'emergency', 'iso3', 'context_date', 'indicator_id',
                'subvariable', 'category', 'admin_level_1'
            ),
        )


class DataCountryLevelQuantiles(models.Model):
    emergency = models.CharField(max_length=50, blank=True, null=True)
    indicator_month = models.DateField()
    indicator_id = models.CharField(max_length=6)
    subvariable = models.CharField(max_length=255)
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
        unique_together = (
            ('region', 'indicator_id', 'subvariable', 'indicator_month', 'category'),
        )


class DataGranular(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    iso3 = models.CharField(max_length=3)
    admin_level_1 = models.CharField(max_length=100)
    indicator_id = models.CharField(max_length=6)
    subvariable = models.CharField(max_length=255)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    thematic = models.CharField(max_length=50, blank=True, null=True)
    thematic_description = models.CharField(max_length=250, blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    topic_description = models.CharField(max_length=250, blank=True, null=True)
    indicator_description = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    direction = models.IntegerField(blank=True, null=True)
    question = models.CharField(max_length=1000, blank=True, null=True)
    indicator_value = models.FloatField(blank=True, null=True)
    nominator = models.BigIntegerField(blank=True, null=True)
    denominator = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    age_group = models.CharField(max_length=10, blank=True, null=True)
    age_info = models.CharField(max_length=20, blank=True, null=True)
    target_group = models.CharField(max_length=40, blank=True, null=True)
    indicator_date = models.DateField(blank=True, null=True)
    indicator_matching = models.CharField(max_length=8, blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    representativeness = models.CharField(max_length=15, blank=True, null=True)
    limitation = models.CharField(max_length=1000, blank=True, null=True)
    indicator_comment = models.CharField(max_length=1000, blank=True, null=True)
    source_id = models.CharField(max_length=5)
    interpolated = models.SmallIntegerField(blank=True, null=True)
    insert_date = models.DateTimeField(blank=True, null=True)
    publish = models.SmallIntegerField(blank=True, null=True)
    indicator_month = models.DateField()
    indicator_publish = models.CharField(max_length=1, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=15, blank=True, null=True)
    display_in_tableau = models.BooleanField(blank=True, null=True)
    income_group = models.CharField(max_length=50, blank=True, null=True)
    fragility_index_fund_for_peace = models.CharField(max_length=50, blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
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
    format = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_data_granular'
        unique_together = (
            (
                'emergency', 'iso3', 'indicator_month', 'indicator_id',
                'subvariable', 'category', 'admin_level_1', 'source_id'
            ),
        )


class EpiData(models.Model):
    iso3 = models.CharField(primary_key=True, max_length=3)
    context_date = models.DateField()
    new_cases = models.FloatField(blank=True, null=True)
    new_cases_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_cases_source = models.CharField(max_length=100, blank=True, null=True)
    total_cases = models.FloatField(blank=True, null=True)
    total_cases_comment = models.CharField(max_length=1000, blank=True, null=True)
    total_cases_source = models.CharField(max_length=100, blank=True, null=True)
    new_deaths = models.FloatField(blank=True, null=True)
    new_deaths_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_deaths_source = models.CharField(max_length=100, blank=True, null=True)
    total_deaths = models.FloatField(blank=True, null=True)
    total_deaths_comment = models.CharField(max_length=1000, blank=True, null=True)
    total_deaths_source = models.CharField(max_length=100, blank=True, null=True)
    total_doses = models.FloatField(blank=True, null=True)
    total_doses_comment = models.CharField(max_length=1000, blank=True, null=True)
    total_doses_source = models.CharField(max_length=100, blank=True, null=True)
    fully_vaccinated_rate = models.FloatField(blank=True, null=True)
    fully_vaccinated_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    fully_vaccinated_rate_source = models.CharField(max_length=100, blank=True, null=True)
    mask_policy = models.FloatField(blank=True, null=True)
    mask_policy_comment = models.CharField(max_length=1000, blank=True, null=True)
    mask_policy_source = models.CharField(max_length=100, blank=True, null=True)
    stay_at_home_requirements = models.FloatField(blank=True, null=True)
    stay_at_home_requirements_comment = models.CharField(max_length=1000, blank=True, null=True)
    stay_at_home_requirements_source = models.CharField(max_length=100, blank=True, null=True)
    stringency = models.FloatField(blank=True, null=True)
    stringency_comment = models.CharField(max_length=1000, blank=True, null=True)
    stringency_source = models.CharField(max_length=100, blank=True, null=True)
    new_cases_per_million = models.FloatField(blank=True, null=True)
    new_cases_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_cases_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    new_deaths_per_million = models.FloatField(blank=True, null=True)
    new_deaths_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    new_deaths_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    economic_support_index = models.FloatField(blank=True, null=True)
    economic_support_index_comment = models.CharField(max_length=1000, blank=True, null=True)
    economic_support_index_source = models.CharField(max_length=100, blank=True, null=True)
    vaccination_policy = models.FloatField(blank=True, null=True)
    vaccination_policy_comment = models.CharField(max_length=1000, blank=True, null=True)
    vaccination_policy_source = models.CharField(max_length=100, blank=True, null=True)
    public_information_campaigns = models.FloatField(blank=True, null=True)
    public_information_campaigns_comment = models.CharField(max_length=1000, blank=True, null=True)
    public_information_campaigns_source = models.CharField(max_length=100, blank=True, null=True)
    vaccinated_rate = models.FloatField(blank=True, null=True)
    vaccinated_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    vaccinated_rate_source = models.CharField(max_length=100, blank=True, null=True)
    boosters_rate = models.FloatField(blank=True, null=True)
    boosters_rate_comment = models.CharField(max_length=1000, blank=True, null=True)
    boosters_rate_source = models.CharField(max_length=100, blank=True, null=True)
    vaccine_supply = models.FloatField(blank=True, null=True)
    vaccine_supply_source = models.CharField(max_length=100, blank=True, null=True)
    hosp_patients = models.FloatField(blank=True, null=True)
    hosp_patients_comment = models.CharField(max_length=1000, blank=True, null=True)
    hosp_patients_source = models.CharField(max_length=100, blank=True, null=True)
    hosp_patients_per_million = models.FloatField(blank=True, null=True)
    hosp_patients_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    hosp_patients_per_million_source = models.CharField(max_length=100, blank=True, null=True)
    icu_patients = models.FloatField(blank=True, null=True)
    icu_patients_comment = models.CharField(max_length=1000, blank=True, null=True)
    icu_patients_source = models.CharField(max_length=100, blank=True, null=True)
    icu_patients_per_million = models.FloatField(blank=True, null=True)
    icu_patients_per_million_comment = models.CharField(max_length=1000, blank=True, null=True)
    icu_patients_per_million_source = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_epi_data'
        unique_together = (('iso3', 'context_date'),)


class EpiDataGlobal(models.Model):
    region = models.CharField(primary_key=True, max_length=255)
    emergency = models.CharField(max_length=50)
    context_date = models.DateField()
    context_indicator_id = models.CharField(max_length=50)
    context_indicator_value = models.FloatField(blank=True, null=True)
    most_recent = models.BooleanField(blank=True, null=True)
    format = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_epi_data_global'
        unique_together = (('region', 'context_date', 'emergency', 'context_indicator_id'),)


class GlobalLevel(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    region = models.TextField()
    indicator_id = models.CharField(max_length=6)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    indicator_description = models.CharField(max_length=250, blank=True, null=True)
    subvariable = models.CharField(max_length=255)
    thematic = models.CharField(max_length=50, blank=True, null=True)
    thematic_description = models.CharField(max_length=250, blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    topic_description = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    indicator_month = models.DateField()
    category = models.CharField(max_length=50)
    indicator_value_global = models.FloatField(blank=True, null=True)
    population_coverage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    std_dev = models.FloatField(blank=True, null=True)
    format = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_global_level'
        unique_together = (
            (
                'emergency', 'region', 'indicator_month',
                'indicator_id', 'subvariable', 'category'
            ),
        )


class Outbreaks(models.Model):
    outbreak = models.CharField(primary_key=True, max_length=50)
    active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_outbreaks'


class RegionLevel(models.Model):
    emergency = models.CharField(primary_key=True, max_length=50)
    region = models.CharField(max_length=15)
    indicator_id = models.CharField(max_length=6)
    indicator_description = models.CharField(max_length=250, blank=True, null=True)
    subvariable = models.CharField(max_length=255)
    indicator_name = models.CharField(max_length=200, blank=True, null=True)
    thematic = models.CharField(max_length=50, blank=True, null=True)
    thematic_description = models.CharField(max_length=250, blank=True, null=True)
    topic = models.CharField(max_length=50, blank=True, null=True)
    topic_description = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    indicator_month = models.DateField()
    category = models.CharField(max_length=50)
    indicator_value_regional = models.FloatField(blank=True, null=True)
    population_coverage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    error_margin = models.FloatField(blank=True, null=True)
    std_dev = models.FloatField(blank=True, null=True)
    format = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_region_level'
        unique_together = (
            (
                'emergency', 'region', 'indicator_month', 'indicator_id',
                'subvariable', 'category'
            ),
        )


class Sources(models.Model):
    source_id = models.CharField(primary_key=True, max_length=5)
    organisation = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    authors = models.CharField(max_length=1000, blank=True, null=True)
    methodology = models.CharField(max_length=250, blank=True, null=True)
    sample_size = models.CharField(max_length=250, blank=True, null=True)
    target_pop = models.CharField(max_length=500, blank=True, null=True)
    scale = models.CharField(max_length=25, blank=True, null=True)
    quality_check = models.CharField(max_length=50, blank=True, null=True)
    impact_factor = models.CharField(max_length=1000, blank=True, null=True)
    access_type = models.CharField(max_length=25, blank=True, null=True)
    source_comment = models.CharField(max_length=5000, blank=True, null=True)
    publication_channel = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=1000, blank=True, null=True)
    source_date = models.DateField(blank=True, null=True)
    key_words = models.CharField(max_length=250, blank=True, null=True)
    source_status = models.CharField(max_length=15, blank=True, null=True)
    frequency = models.CharField(max_length=15, blank=True, null=True)
    sample_type = models.CharField(max_length=25, blank=True, null=True)
    publish = models.CharField(max_length=25, blank=True, null=True)
    insert_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_sources'


class CountryFilterOptions(models.Model):
    iso3 = models.CharField(primary_key=True, max_length=3)
    emergency = models.CharField(max_length=50)
    indicator_id = models.CharField(max_length=6, default='')
    indicator_description = models.CharField(max_length=250, blank=True, null=True)
    subvariable = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 't_country_indicator_options'
