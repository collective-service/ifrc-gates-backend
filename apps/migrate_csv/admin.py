from functools import reduce

from django.contrib import admin
from django.urls import path
from django.utils import timezone
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib import messages

from admin_auto_filters.filters import AutocompleteFilterFactory

from config.utils import get_admin_url

from .views import CustomAutocompleteJsonView
from .models import (
    DataImport,
    ImportUserDataPreview,
    ImportUserSourceDataPreview,
)


@admin.register(DataImport)
class DataImportAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'status',
        'description',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at',
        'assigned_to',
        'assigned_at',
        'reviewed_count',
        'migrated_by',
        'migrated_at',
    ]
    autocomplete_fields = (
        'created_by',
        'updated_by',
        'assigned_to',
    )
    search_fields = ['created_by__full_name']
    readonly_fields = [
        'status',
        'created_by', 'created_at',
        'updated_by', 'updated_at',
        'migrated_at', 'migrated_by',
        'assigned_at',
    ]
    list_filter = [
        AutocompleteFilterFactory('Created By', 'created_by'),
        'file_type',
        'status',
    ]

    def get_queryset(self, request):
        reviewed_count_annotate = reduce(
            lambda a, b: a + b,
            [
                models.functions.Coalesce(
                    models.Subquery(
                        model.objects.filter(
                            importer=models.OuterRef('pk'),
                            is_reviewed=True,
                        ).values('importer').order_by().annotate(
                            count=models.Count('id'),
                        ).values('count')[:1], output_field=models.IntegerField()
                    ), 0
                )
                for model in DataImport.FILE_TYPE_TO_MODEL_MAP.values()
            ],
        )
        return super().get_queryset(request).annotate(reviewed_count=reviewed_count_annotate)

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.created_by == request.user
        return True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'custom_autocomplete_search/',
                self.admin_site.admin_view(
                    CustomAutocompleteJsonView.as_view(admin_site=self.admin_site),
                ),
                name='custom_autocomplete_search'
            ),
        ]
        return custom_urls + urls

    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Non-editable on update
            return [
                *self.readonly_fields,
                'file',
                'file_type',
            ]
        # Non-editable on add
        return [
            'assigned_to',
            *self.readonly_fields,
        ]

    def created_by(self, obj):
        return obj.created_by and obj.created_by.full_name

    def updated_by(self, obj):
        return obj.updated_by and obj.updated_by.full_name

    def assigned_to(self, obj):
        return obj.assigned_to and obj.assigned_to.full_name

    @admin.display
    def reviewed_count(self, obj):
        return obj.reviewed_count

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if obj.pk is None:
            obj.created_by = request.user
        else:
            existing_obj = DataImport.objects.get(pk=obj.pk)
            if obj.assigned_to is None:
                obj.assigned_at = None
            elif existing_obj.assigned_to != obj.assigned_to:
                obj.assigned_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.action(description='Bulk mark previews as reviewed.')
def bulk_review_true(modeladmin, request, queryset):
    count = queryset.update(
        is_reviewed=True,
        reviewed_by=request.user,
        reviewed_at=timezone.now(),
    )
    messages.add_message(
        request, messages.INFO,
        mark_safe(_('Successfully marked %s previews') % (count))
    )


@admin.action(description='Bulk mark previews as not reviewed.')
def bulk_review_false(modeladmin, request, queryset):
    count = queryset.update(
        is_reviewed=False,
        reviewed_by=None,
        reviewed_at=None,
    )
    messages.add_message(
        request, messages.INFO,
        mark_safe(_('Successfully unmarked %s previews') % (count))
    )


class ImportUserDataPreviewBaseAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = [
        'id',
        'importer',
        'is_reviewed',
        'no_outlier',
        'reviewed_at',
    ]
    readonly_fields = (
        'importer',
        'reviewed_by',
        'reviewed_at',
        'no_outlier',
        'outlier_remarks',
    )
    exclude = ('outlier_data',)
    list_filter = [
        AutocompleteFilterFactory('Reviewed by', 'reviewed_by'),
        AutocompleteFilterFactory('CSV', 'importer', 'admin:custom_autocomplete_search', True),
        'no_outlier',
        'is_reviewed',
    ]
    actions = [bulk_review_true, bulk_review_false]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            importer__status=DataImport.Status.PREVIEW,
            importer__assigned_to=request.user,
        ).select_related('importer')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and request.path == get_admin_url(DataImport, 'changelist'):
            reviewd_changed_previews = type(obj).objects.filter(
                importer=obj.importer,
                is_reviewed=True,
            )
            return (
                not reviewd_changed_previews.exists() and
                obj.importer.created_by == request.user
            )
        return True

    @admin.display
    def outlier_remarks(self, obj):
        outlier_columns = obj.outlier_data or []
        if outlier_columns:
            return mark_safe(
                '<pre>' +
                'Outlier columns:\n' +
                '\n'.join(
                    f'- {col}'
                    for col in outlier_columns
                ) +
                '</pre>'
            )
        return '-'

    def save_model(self, request, obj, form, change):
        # On Update
        if obj.pk is not None:
            existing_obj = type(obj).objects.get(pk=obj.pk)
            if not obj.is_reviewed:
                obj.reviewed_by = None
                obj.reviewed_at = None
            elif existing_obj.is_reviewed != obj.is_reviewed:
                obj.reviewed_by = request.user
                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(ImportUserDataPreview)
class ImportUserDataPreviewAdmin(ImportUserDataPreviewBaseAdmin):
    list_display = [
        *ImportUserDataPreviewBaseAdmin.list_display,
        *ImportUserDataPreview.CSV_HEADERS,
    ]


@admin.register(ImportUserSourceDataPreview)
class ImportUserSourceDataPreviewAdmin(ImportUserDataPreviewBaseAdmin):
    list_display = [
        *ImportUserDataPreviewBaseAdmin.list_display,
        *ImportUserSourceDataPreview.CSV_HEADERS,
    ]
