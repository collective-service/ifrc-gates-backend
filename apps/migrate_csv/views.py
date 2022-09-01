from functools import cache
from urllib.parse import urlparse

from django.contrib.admin.views.autocomplete import AutocompleteJsonView as Base

from config.utils import get_admin_url
from apps.migrate_csv.models import (
    DataImport,
    ImportUserSourceDataPreview,
    ImportUserDataPreview,
)


@cache
def get_data_preview_admin_urls_file_type():
    return {
        get_admin_url(model, 'changelist'): DataImport.MODEL_TO_FILE_TYPE_MAP[model]
        for model in [
            ImportUserSourceDataPreview,
            ImportUserDataPreview,
        ]
    }


class CustomAutocompleteJsonView(Base):
    def get_queryset(self):
        qs = super().get_queryset()
        referer_path = urlparse(self.request.headers.get('Referer', '')).path
        preview_url_map = get_data_preview_admin_urls_file_type()
        if referer_path in preview_url_map:
            if qs.model == DataImport:
                return qs.filter(
                    assigned_to=self.request.user,
                    file_type=get_data_preview_admin_urls_file_type()[referer_path],
                    status=DataImport.Status.PREVIEW,
                )
        return qs
