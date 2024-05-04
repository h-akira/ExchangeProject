from django.contrib import admin
from .models import CategoryTable, ChartTable, LinkTable

# Register your models here.
admin.site.register(CategoryTable)
admin.site.register(ChartTable)
admin.site.register(LinkTable)
