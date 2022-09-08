import logging
import pandas as pd
from celery import shared_task

from .models import DataImport
from .outlier_detect import detect_outliers

logger = logging.getLogger(__name__)


def format_column(column):
    # Lower all columns name
    return column.lower().replace(' ', '_')


@shared_task
def process_data_import(pk):
    data_import = DataImport.objects.get(pk=pk)
    if data_import.status not in [DataImport.Status.FAILED_PROCESSING, DataImport.Status.PENDING]:
        logger.warning(f'Not processing with DataImport(pk:{pk}) status: {data_import.status}')
        return

    try:
        PREVIEW_MODEL = data_import.preview_model
        existing_preview = PREVIEW_MODEL.objects.filter(importer=data_import)
        if existing_preview.exists():
            logger.warning(f'Not processing with DataImport(pk:{pk}) Preview already exists: {existing_preview.count()}')
            return

        df = pd.read_csv(data_import.file, delimiter=',')
        df = df.rename(columns=format_column)
        outliers, _ = detect_outliers(df, PREVIEW_MODEL)
        new_preview_objects = []
        for index, row in df.iterrows():
            outlier_data = list({
                column
                for column, indexes in outliers.items()
                if index in indexes   # indexes is set
            })
            new_preview_objects.append(
                PREVIEW_MODEL(
                    importer=data_import,
                    no_outlier=not outlier_data,
                    outlier_data=outlier_data,
                    **{
                        column: row[column]
                        for column in PREVIEW_MODEL.CSV_HEADERS
                    }
                )
            )
        PREVIEW_MODEL.objects.bulk_create(new_preview_objects)
        data_import.status = DataImport.Status.PREVIEW
    except Exception:
        logger.error(f'Failed to process DataImport(pk: {pk})', exc_info=True)
        data_import.status = DataImport.Status.FAILED_PROCESSING
    data_import.save(update_fields=('status',))
