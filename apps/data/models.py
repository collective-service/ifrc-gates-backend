from django.db import models


class IndicatorData(models.Model):
    indicator_value = models.FloatField(null=True)

    class Meta:
        managed = False
        db_table = 'indicator_data'
