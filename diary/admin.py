from django.contrib import admin
from .models import EventTable, DiaryTable
from markdownx.admin import MarkdownxModelAdmin



# Register your models here.
admin.site.register(EventTable)
admin.site.register(DiaryTable, MarkdownxModelAdmin)  # 追記
