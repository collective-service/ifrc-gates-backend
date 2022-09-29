from typing import List, Tuple

from django import forms
from django.utils.translation import gettext_lazy as _

from tinymce.widgets import TinyMCE
from config.caches import redis_cache_func, CacheKey

from .models import Narratives, DataCountryLevel


class NarrativesChoices():

    @staticmethod
    def _get_choices_from_data_country_level(value, label) -> List[Tuple[str, str]]:
        return DataCountryLevel.objects.values_list(value, label).order_by(label).distinct()

    @classmethod
    @redis_cache_func(CacheKey.AdminNarrativeChoices.ISO3, CacheKey.AdminNarrativeChoices.TTL)
    def iso3(cls) -> List[Tuple[str, str]]:
        return cls._get_choices_from_data_country_level('iso3', 'country_name')

    @classmethod
    @redis_cache_func(CacheKey.AdminNarrativeChoices.THEMATIC, CacheKey.AdminNarrativeChoices.TTL)
    def thematic(cls) -> List[Tuple[str, str]]:
        return cls._get_choices_from_data_country_level('thematic', 'thematic')

    @classmethod
    @redis_cache_func(CacheKey.AdminNarrativeChoices.TOPIC, CacheKey.AdminNarrativeChoices.TTL)
    def topic(cls) -> List[Tuple[str, str]]:
        return cls._get_choices_from_data_country_level('topic', 'topic')

    @classmethod
    @redis_cache_func(CacheKey.AdminNarrativeChoices.INDICATOR_ID, CacheKey.AdminNarrativeChoices.TTL)
    def indicator_id(cls) -> List[Tuple[str, str]]:
        return cls._get_choices_from_data_country_level('indicator_id', 'indicator_name')


class NarrativesForm(forms.ModelForm):
    iso3 = forms.ChoiceField(choices=[], required=False)
    thematic = forms.ChoiceField(choices=[], required=False)
    topic = forms.ChoiceField(choices=[], required=False)
    indicator_id = forms.ChoiceField(choices=[], required=False)
    narrative = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label=_("Narrative"))

    class Meta:
        model = Narratives
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, get_choices in [
            ('iso3', NarrativesChoices.iso3),
            ('thematic', NarrativesChoices.thematic),
            ('topic', NarrativesChoices.topic),
            ('indicator_id', NarrativesChoices.indicator_id),
        ]:
            _field = self.fields[field]
            _field.choices = get_choices()
            if not _field.required:
                _field.choices = [
                    ('', _('-- Not selected --')),
                    *_field.choices,
                ]
