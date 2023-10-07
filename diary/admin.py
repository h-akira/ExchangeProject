from django.contrib import admin
from .models import EventTable, DiaryTable

# Register your models here.
admin.site.register(EventTable)
admin.site.register(DiaryTable)
