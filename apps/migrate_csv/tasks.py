from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(name="migrate_main_file_in_preview_table")
def migrate_main_file_in_preview_table(file_id):
    print(file_id)
    return True


@shared_task(name="migrate_supplementary_file_in_preview_table")
def migrate_supplementary_file_in_preview_table(file_id):
    print(file_id)
    return True
