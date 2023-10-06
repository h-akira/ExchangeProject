from django.db import models

class ExchangeDataTable(models.Model):
  dt = models.DateTimeField()
  pair = models.CharField(max_length=15)  # USDJPYなど（/なし）
  Open = models.FloatField()
  High = models.FloatField()
  Low = models.FloatField()
  Close = models.FloatField()
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["dt", "pair"],
        name="time_unique"
      )
    ]

