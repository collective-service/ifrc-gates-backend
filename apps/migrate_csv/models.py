import csv
import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


def file_upload_to(instance, filename):
    date_str = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
    return f'csv-files/{date_str}/{filename}'


def csv_file_validator(document, required_headers):
    # TODO: Fix import maybe use utils.py
    from .tasks import format_column

    try:
        dialect = csv.Sniffer().sniff(document.read(1024).decode('utf-8'))
        document.seek(0, 0)
    except (csv.Error, UnicodeDecodeError):
        raise ValidationError(_('Not a valid CSV file'))
    reader = csv.reader(document.read().decode('utf-8').splitlines(), dialect)
    for index, row in enumerate(reader):
        # check that all headers are present
        if index == 0:
            csv_headers = [
                format_column(header_name)
                for header_name in row
                if header_name
            ]
            missing_headers = set(required_headers) - set(csv_headers)
            additional_headers = set(csv_headers) - set(required_headers)
            error_messages = []
            if missing_headers:
                _headers = ', '.join(missing_headers)
                error_messages.append(_('Missing headers: %s' % (_headers)))
            if additional_headers:
                _headers = ', '.join(additional_headers)
                error_messages.append(_('Additional headers: %s' % (_headers)))
            if error_messages:
                error_messages.append(
                    _(
                        'NOTE: In backend, columns are lowercased and spaces are replaced with _. '
                        'Eg: Age info -> age_info'
                    )
                )
                raise ValidationError(error_messages)
            break
    document.seek(0, 0)
    return True


class DataImportPreviewBase(models.Model):
    CSV_HEADERS = []
    DATA_DB_TABLE_NAME = None
    DATA_DB_COLUMN_MAP = {}

    importer = models.ForeignKey(
        'DataImport',
        verbose_name=_('Csv file form'),
        related_name='%(class)s_previews',
        on_delete=models.CASCADE
    )
    # Review attributes
    is_reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User,
        verbose_name=_('Reviewed By'),
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    reviewed_at = models.DateTimeField(verbose_name=_('Reviewed at'), blank=True, null=True)

    # Outlier attributes
    no_outlier = models.BooleanField(verbose_name=_('No outlier'), default=False)
    outlier_data = models.JSONField(default=list, blank=True)

    class Meta:
        abstract = True


# ---- Previews [Start]

class ImportUserDataPreview(DataImportPreviewBase):
    CSV_HEADERS = [
        # Make sure all columns are lowercase here.
        'source_id',
        'outbreak',
        'country',
        'iso3',
        'adminlevel1',
        'indicator',
        'indicator_id',
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
        'topic',
        'thematic',
        'subindicator',
    ]

    # WIP: Database meta
    DATA_DB_TABLE_NAME = 'indicator_data'
    DATA_DB_COLUMN_MAP = {
        # CSV Column: DB Column
        'adminlevel1': 'admin_level_1',
        'age_group': 'age_group',
        'age_info': 'age_info',
        'area': 'area',
        'comment': None,
        'contribution_marker': None,
        'country': None,
        'date': 'insert_date',
        'denominator': 'denominator',
        'errormargin': 'error_margin',
        'gender': 'gender',
        'indicator': None,
        'indicator_id': 'indicator_id',
        'iso3': 'iso3',
        'limitation': 'limitation',
        'nominator': 'nominator',
        'outbreak': None,
        'percentage': None,
        'questions': 'question',
        'representativeness': 'representativeness',
        'source_id': 'source_id',
        'subindicator': None,
        'target_group': 'target_group',
        'thematic': None,
        'topic': None,
        # Additional columns in the Database
        # - category
        # - emergency
        # - indicator_comment
        # - indicator_date
        # - indicator_matching
        # - indicator_value
        # - interpolated
        # - publish
        # - subvariable
    }

    source_id = models.CharField(max_length=255, blank=True, verbose_name=_('Source id'))
    outbreak = models.CharField(max_length=255, blank=True, verbose_name=_('Outbreak'))
    country = models.CharField(max_length=255, blank=True, verbose_name=_('Country'))
    iso3 = models.CharField(max_length=255, blank=True, verbose_name=_('ISO3'))
    adminlevel1 = models.CharField(max_length=255, blank=True, verbose_name=_('Admin Level 1'))
    indicator = models.CharField(max_length=255, blank=True, verbose_name=_('Indicator'))
    indicator_id = models.CharField(max_length=255, blank=True, verbose_name=_('Indicator id'))
    dimension = models.CharField(max_length=255, blank=True, verbose_name=_('Dimension'))
    questions = models.CharField(max_length=255, blank=True, verbose_name=_('Questions'))
    percentage = models.FloatField(blank=True, verbose_name=_('Percentage'))
    nominator = models.IntegerField(blank=True, verbose_name=_('Nominator'))
    denominator = models.IntegerField(blank=True, verbose_name=_('Denominator'))
    errormargin = models.FloatField(blank=True, verbose_name=_('Error margin'))
    limitation = models.IntegerField(blank=True, verbose_name=_('Limitation'))
    gender = models.CharField(max_length=255, blank=True, verbose_name=_('Gender'))
    age_group = models.CharField(max_length=255, blank=True, verbose_name=_('Age group'))
    age_info = models.CharField(max_length=255, blank=True, verbose_name=_('Age info'))
    target_group = models.CharField(max_length=255, blank=True, verbose_name=_('Target group'))
    date = models.DateField(blank=True, verbose_name=_('Date'))
    contribution_marker = models.CharField(max_length=255, blank=True, verbose_name=_('Contribution marker'))
    representativeness = models.CharField(max_length=255, blank=True, verbose_name=_('Representativeness'))
    area = models.CharField(max_length=255, blank=True, verbose_name=_('Area'))
    comment = models.CharField(max_length=255, blank=True, verbose_name=_('Comment'))
    topic = models.CharField(max_length=255, blank=True, verbose_name=_('Topic'))
    thematic = models.CharField(max_length=255, blank=True, verbose_name=_('Thematic'))
    subindicator = models.CharField(max_length=255, blank=True, verbose_name=_('Sub indicator'))

    def __str__(self):
        return f'{self.outbreak} - {self.country} - {self.iso3}'


class ImportUserSourceDataPreview(DataImportPreviewBase):
    CSV_HEADERS = [
        'source_id',
        'organisation',
        'title',
        'details',
        'authors',
        'sample_type',
        'survey_method',
        'sample',
        'targetpop',
        'scale',
        'quality_check',
        'data_access_type',
        'comment',
        'source',
        'link',
        'source_date',
        'key_words',
    ]

    # WIP: Database meta
    DATA_DB_TABLE_NAME = 'sources'
    DATA_DB_COLUMN_MAP = {
        # CSV Column: DB Column
        'data_access_type': 'access_type',
        'authors': 'authors',
        'comment': None,
        'details': 'details',
        'key_words': 'key_words',
        'link': 'link',
        'organisation': 'organisation',
        'quality_check': 'quality_check',
        'sample': 'sample_size',
        'sample_type': 'sample_type',
        'scale': 'scale',
        'source': None,
        'source_date': 'source_date',
        'source_id': 'source_id',
        'survey_method': None,
        'targetpop': 'target_pop',
        'title': 'title',
        # Addtional columns in DB
        # - frequency
        # - impact_factor
        # - insert_date
        # - methodology
        # - publication_channel
        # - publish
        # - source_comment
        # - source_status
    }

    source_id = models.CharField(max_length=255, blank=True, verbose_name=_('Source ID'))
    organisation = models.CharField(max_length=255, blank=True, verbose_name=_('Organisation'))
    title = models.CharField(max_length=255, blank=True, verbose_name=_('Title'))
    details = models.TextField(blank=True, verbose_name=_('Details'))
    authors = models.CharField(max_length=255, blank=True, verbose_name=_('Authors'))
    sample_type = models.CharField(max_length=255, blank=True, verbose_name=_('Sample type'))
    survey_method = models.CharField(max_length=255, blank=True, verbose_name=_('Survey Method'))
    sample = models.IntegerField(blank=True, verbose_name=_('Sample'))
    targetpop = models.CharField(max_length=255, blank=True, verbose_name=_('TargetPop'))
    scale = models.CharField(max_length=255, blank=True, verbose_name=_('Scale'))
    quality_check = models.CharField(max_length=255, blank=True, verbose_name=_('Quality Check'))
    data_access_type = models.CharField(max_length=255, blank=True, verbose_name=_('Data Access Type'))
    comment = models.CharField(max_length=255, blank=True, verbose_name=_('Comment'))
    source = models.CharField(max_length=255, blank=True, verbose_name=_('Source'))
    link = models.CharField(max_length=255, blank=True, verbose_name=_('Link'))
    source_date = models.DateField(blank=True, verbose_name=_('Source Date'))
    key_words = models.CharField(max_length=255, blank=True, verbose_name=_('Key Words'))

    def __str__(self):
        return f'{self.source_id} - {self.organisation} - {self.title}'


# ---- Previews [End]
class DataImport(models.Model):
    class FileType(models.IntegerChoices):
        USER = 0, _('RCCE Data Input User')
        USER_SOURCE = 1, _('RCCE Data Input User Sources')

    class Status(models.IntegerChoices):
        PENDING = 0, _('Pending')
        PROCESSING = 1, _('Processing (Extraction + Outlier Detection)')
        PREVIEW = 2, _('Preview')
        MIGRATED = 3, _('Migrated')
        CANCELED = 4, _('Canceled')
        # Failed status
        FAILED_PROCESSING = 500, _('Failed Processing')
        FAILED_MIGRATING = 501, _('Failed Migrating')

    FILE_TYPE_TO_MODEL_MAP = {
        FileType.USER: ImportUserDataPreview,
        FileType.USER_SOURCE: ImportUserSourceDataPreview,
    }

    MODEL_TO_FILE_TYPE_MAP = {
        model: file_type
        for file_type, model in FILE_TYPE_TO_MODEL_MAP.items()
    }

    FAILED_STATUS = [
        Status.FAILED_MIGRATING,
        Status.FAILED_PROCESSING,
    ]

    file = models.FileField(verbose_name=_('CSV file'), upload_to=file_upload_to)
    # TODO: Maybe add checksum as well to avoid uploading same file twice.
    file_type = models.SmallIntegerField(choices=FileType.choices)
    status = models.SmallIntegerField(choices=Status.choices, default=Status.PENDING)
    description = models.TextField(blank=True, verbose_name=_('Description'))

    # Creation
    created_by = models.ForeignKey(
        User,
        verbose_name=_('Created By'),
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    # Update
    updated_by = models.ForeignKey(
        User,
        verbose_name=_('Updated by'),
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
    # Assigned
    assigned_to = models.ForeignKey(
        User,
        verbose_name=_('Assigned to'),
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    assigned_at = models.DateTimeField(verbose_name=_('Assigned at'), null=True, blank=True)
    # Migration
    migrated_by = models.ForeignKey(
        User,
        verbose_name=_('Migrated by'),
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    migrated_at = models.DateTimeField(verbose_name=_('Migrated at'), null=True, blank=True)

    def __str__(self):
        return self.file.name.split('/')[-1]

    @property
    def preview_model(self):
        return self.FILE_TYPE_TO_MODEL_MAP[DataImport.FileType(self.file_type)]

    def clean(self):
        if self.pk is None and self.file_type is not None:
            # Validate CSV File on creation.
            required_headers = self.preview_model.CSV_HEADERS
            csv_file_validator(self.file, required_headers)

    def save(self, *args, **kwargs):
        from .tasks import process_data_import
        new = False
        if self.pk is None:
            new = True
        super().save(*args, **kwargs)
        if new:
            # process_data_import.delay(self.pk)
            process_data_import(self.pk)
