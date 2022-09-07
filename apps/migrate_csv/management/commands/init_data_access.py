from functools import cache

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_permission_codename, get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


from apps.migrate_csv.models import (
    DataImport,
    ImportUserDataPreview,
    ImportUserSourceDataPreview,
)


def get_permission(action: str, content_type: ContentType) -> Permission:
    codename = get_permission_codename(action, content_type.model_class()._meta)
    return Permission.objects.get(
        codename=codename,
        content_type=content_type,
    )


class Command(BaseCommand):
    help = 'Add framework owner membership for all creators of frameworks'

    @cache
    @staticmethod
    def get_data_importer_group():
        group, _ = Group.objects.get_or_create(name='Data Importer')
        return group

    @cache
    @staticmethod
    def get_data_reviewer_group():
        group, _ = Group.objects.get_or_create(name='Data Reviewer')
        return group

    def handle(self, *args, **options):
        DataImportContentType = ContentType.objects.get_for_model(DataImport)
        UserContentType = ContentType.objects.get_for_model(get_user_model())
        PREVIEW_MODEL_CONTENT_TYPE = [
            ContentType.objects.get_for_model(ImportUserDataPreview),
            ContentType.objects.get_for_model(ImportUserSourceDataPreview),
        ]

        di_group = self.get_data_importer_group()
        dr_group = self.get_data_reviewer_group()

        for group, permission_set in [
            # Importer group
            [
                di_group, [
                    [DataImportContentType, ['add', 'view', 'delete']],
                ]
            ],
            # Reviewer group
            [
                dr_group, [
                    [DataImportContentType, ['view', 'change']],
                    [UserContentType, ['view']],
                    *[
                        [content_type, ['view', 'change', 'delete']]
                        for content_type in PREVIEW_MODEL_CONTENT_TYPE
                    ],
                ]
            ],
        ]:
            for (model_content_type, permissions_str) in permission_set:
                permissions = [
                    get_permission(perm_str, model_content_type)
                    for perm_str in permissions_str
                ]
                group.permissions.add(*permissions)
