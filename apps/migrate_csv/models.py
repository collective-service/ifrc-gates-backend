from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def file_upload_to(instance, filename):
    date_str = timezone.now().strftime('%Y-%m-%d-%H-%M-%S')
    return f'csv-files/{date_str}/{filename}'


class CsvFile(models.Model):

    class FileType(models.TextChoices):
        MAIN = 'main', _('Main')
        SUPPLEMENTARY = 'supplementary', _('Supplementary')

    file = models.FileField(
        verbose_name=_('Csv file'),
        upload_to=file_upload_to,
    )
    file_type = models.CharField(
        max_length=20,
        choices=FileType.choices,
        default=FileType.MAIN,
    )
    created_by = models.ForeignKey(
        User,
        verbose_name=_('Created By'),
        blank=True, null=True,
        related_name='created_csv_files',
        on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name=_('Updated by'),
        blank=True, null=True,
        related_name='updated_csv_files',
        on_delete=models.SET_NULL
    )
    assigned_to = models.ForeignKey(
        User,
        verbose_name=_('Assigned to'),
        blank=True, null=True,
        related_name='assigned_csv_files',
        on_delete=models.SET_NULL
    )
    migrated_by = models.ForeignKey(
        User,
        verbose_name=_('Migrated by'),
        blank=True, null=True,
        related_name='migrated_by',
        on_delete=models.SET_NULL
    )
    migrated_in_preview_table = models.BooleanField(default=False)
    migrated_in_production = models.BooleanField(default=False)
    migrated_at = models.DateTimeField(verbose_name=_('Migrated at'), null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), default=timezone.now)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
    description = models.TextField(
        blank=True, verbose_name=_('Description')
    )
    assigned_at = models.DateTimeField(verbose_name=_('Assigned at'), null=True, blank=True)

    def __str__(self):
        return self.file.name


class CsvFilePreview(models.Model):

    outbreak = models.CharField(max_length=255, blank=True, verbose_name=_('Outbreak'))
    country = models.CharField(max_length=255, blank=True, verbose_name=_('Country'))
    iso3 = models.CharField(max_length=255, blank=True, verbose_name=_('ISO3'))
    adminlevel1 = models.CharField(max_length=255, blank=True, verbose_name=_('Admin Level 1'))
    indicator = models.CharField(max_length=255, blank=True, verbose_name=_('Indicator'))
    indicator_id = models.CharField(max_length=255, blank=True, verbose_name=_('Indicator id'))
    dimension = models.CharField(max_length=255, blank=True, verbose_name=_('Dimension'))
    questions = models.CharField(max_length=255, blank=True, verbose_name=_('Questions'))
    percentage = models.CharField(max_length=255, blank=True, verbose_name=_('Percentage'))
    nominator = models.IntegerField(blank=True, verbose_name=_('Nominator'))
    denominator = models.IntegerField(blank=True, verbose_name=_('Denominator'))
    gender = models.CharField(max_length=255, blank=True, verbose_name=_('Gender'))
    age_group = models.CharField(max_length=255, blank=True, verbose_name=_('Age group'))
    age_info = models.CharField(max_length=255, blank=True, verbose_name=_('Age info'))
    target_group = models.CharField(max_length=255, blank=True, verbose_name=_('Target group'))
    date = models.DateField(blank=True, verbose_name=_('Date'))
    contribution_marker = models.CharField(max_length=255, blank=True, verbose_name=_('Contribution marker'))
    errormargin = models.CharField(max_length=255, blank=True, verbose_name=_('Error margin'))
    representativeness = models.CharField(max_length=255, blank=True, verbose_name=_('Representativeness'))
    area = models.CharField(max_length=255, blank=True, verbose_name=_('Area'))
    limitation = models.CharField(max_length=255, blank=True, verbose_name=_('Limitation'))
    comment = models.CharField(max_length=255, blank=True, verbose_name=_('Comment'))
    source_id = models.CharField(max_length=255, blank=True, verbose_name=_('Source id'))
    topic = models.CharField(max_length=255, blank=True, verbose_name=_('Topic'))
    thematic = models.CharField(max_length=255, blank=True, verbose_name=_('Thematic'))
    subindicator = models.CharField(max_length=255, blank=True, verbose_name=_('Sub indicator'))

    # Extra fields
    is_outlier = models.BooleanField(default=False)
    outlier_remarks = models.CharField(max_length=255, blank=True)

    csv_file = models.ForeignKey(
        'migrate_csv.CsvFile',
        verbose_name=_('Csv file form'),
        related_name='csv_file_previews',
        on_delete=models.CASCADE
    )
    reviewed_by = models.ForeignKey(
        User,
        verbose_name=_('Reviewed By'),
        blank=True, null=True,
        related_name='reviewed_csv_previews',
        on_delete=models.SET_NULL
    )
    reviewed_at = models.DateTimeField(verbose_name=_('Reviewed at'), blank=True)

    def __str__(self):
        return f'{self.outbreak} - {self.country} - {self.iso3}'
