from django import forms
from .models import DiaryTable
from markdownx.widgets import MarkdownxWidget

class DiaryForm(forms.ModelForm):
  class Meta:
    model = DiaryTable
    fields = ("text",)
    widgets = {
      'text': MarkdownxWidget(
        attrs={
          'class': 'dynamic-textarea padding-all'
        }
      )
    }
