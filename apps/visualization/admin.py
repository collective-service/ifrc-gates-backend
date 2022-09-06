from django.contrib import admin

from .models import Narratives
from .forms import NarrativesForm


@admin.register(Narratives)
class NarrativesAdmin(admin.ModelAdmin):
    form = NarrativesForm
    list_display = ('__str__', 'iso3', 'thematic', 'topic', 'indicator_id', 'insert_date',)
