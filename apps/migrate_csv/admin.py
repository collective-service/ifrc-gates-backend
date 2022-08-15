from django.contrib import admin
from django.utils import timezone
from apps.migrate_csv.models import CsvFile, CsvFilePreview
from apps.migrate_csv.forms import CsvFileForm


class CsvFileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'migrated_in_preview_table',
        'migrated_in_production',
        'created_at',
        'updated_at',
        'description',
        'created_by',
        'updated_by',
        'assigned_to',
        'assigned_at',
        'migrated_at',
        'migrated_by',
    ]
    autocomplete_fields = ('created_by', 'updated_by', 'assigned_to')
    search_fields = ['created_by__full_name']
    readonly_fields = [
        'migrated_in_preview_table',
        'migrated_in_production',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'assigned_at',
        'migrated_at',
        'migrated_by',
    ]
    list_filter = [
        'created_by',
        'migrated_in_production',
    ]
    form = CsvFileForm

    def created_by(self, obj):
        return obj.created_by.full_name

    def updated_by(self, obj):
        return obj.updated_by.full_name

    def assigned_to(self, obj):
        return obj.assigned_to.full_name

    def save_model(self, request, obj, form, change):
        if obj.id is not None:
            obj.updated_by = request.user
            if obj.assigned_to:
                obj.assigned_at = timezone.now()
        else:
            obj.created_by = request.user
            if obj.assigned_to:
                obj.assigned_at = timezone.now()
        obj.save()


class CsvFilePreviewAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'outbreak',
        'country',
        'iso3',
        'adminlevel1',
        'indicator',
        'indicator_id',
        'dimension',
        'questions',
        'percentage',
        'nominator',
        'denominator',
        'gender',
        'age_group',
        'age_info',
        'target_group',
        'date',
        'contribution_marker',
        'errormargin',
        'representativeness',
        'area',
        'limitation',
        'comment',
        'source_id',
        'csv_file',
        'reviewed_by',
        'reviewed_at',

    ]
    autocomplete_fields = ('csv_file', 'reviewed_by', )
    list_filter = [
        'reviewed_by',
    ]


admin.site.register(CsvFile, CsvFileAdmin)
admin.site.register(CsvFilePreview, CsvFilePreviewAdmin)
