from django.contrib import admin
from .models import DiaryTable
from markdownx.admin import MarkdownxModelAdmin



# Register your models here.
admin.site.register(DiaryTable, MarkdownxModelAdmin)  # 追記
