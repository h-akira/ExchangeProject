from django.contrib import admin
from .models import ExchangeDataTable, EventTable

# Register your models here.
admin.site.register(EventTable)
admin.site.register(ExchangeDataTable)
