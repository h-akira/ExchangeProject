from django import forms
from .models import EventCommentTable
from markdownx.widgets import MarkdownxWidget

class EventCommentForm(forms.ModelForm):
  class Meta:
    model = EventCommentTable
    fields = ("text",)
    widgets = {
      'text': MarkdownxWidget(
        attrs={
          'class': 'dynamic-textarea padding-all'
        }
      )
    }
