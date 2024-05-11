from django.db import models
from accounts.models import CustomUser 

# Create your models here.

SOURCE_CHOICES = [
  ('yahoo finance', 'Yahoo Finance'),
  ('tradingview', 'TradingView'),
]

class CategoryTable(models.Model):
  name = models.CharField(max_length=127)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  description = models.TextField(null=True, blank=True)
  def __str__(self):
    return self.name

class ChartTable(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=127)
  source = models.CharField(max_length=63, choices=SOURCE_CHOICES)
  symbol = models.CharField(max_length=63)
  priority = models.IntegerField(default=0)
  category = models.ForeignKey(CategoryTable, on_delete=models.CASCADE, null=True, blank=True)
  def __str__(self):
    return self.name
  def save(self, *args, **kwargs):
    if self.category.user != self.user:
      print(self.user, self.category.user)
      raise ValueError("The category does not belong to the user")
    super().save(*args, **kwargs)

class LinkTable(models.Model):
  name = models.CharField(max_length=127)
  chart = models.ForeignKey(ChartTable, on_delete=models.CASCADE)
  url = models.URLField()
  description = models.TextField(null=True, blank=True)
  def __str__(self):
    return self.name
