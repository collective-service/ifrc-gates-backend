# Generated by Django 4.1.1 on 2022-11-29 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('migrate_csv', '0005_rename_countryfilteroptions_cachedcountryfilteroptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataimport',
            name='file_type',
            field=models.SmallIntegerField(choices=[(0, 'Collective Service Data Input User'), (1, 'Collective Service Data Input User Sources')]),
        ),
    ]