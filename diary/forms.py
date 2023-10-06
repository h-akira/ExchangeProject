from django import forms
from .models import DiaryTable

class DiaryForm(forms.ModelForm):
  class Meta:
    model = DiaryTable
    fields = ("text",)
    widgets = {
      'text': forms.Textarea(
        attrs={
          'class': 'dynamic-textarea padding-all'
        }
      )
    }
