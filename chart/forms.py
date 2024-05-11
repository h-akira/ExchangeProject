from django import forms
from django.forms import modelformset_factory
from .models import ChartTable, CategoryTable

class ChartEditForm(forms.ModelForm):
  class Meta:
    model = ChartTable
    fields = ["name", "source", "symbol", "category", "priority"]
    widgets = {
      'name': forms.TextInput(attrs={'style': 'width: 200px;'}),
      'symbol': forms.TextInput(attrs={'style': 'width: 200px;'}),
      'priority': forms.NumberInput(attrs={'style': 'width: 50px;'}),
    }
  def __init__(self, user, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['category'].queryset = CategoryTable.objects.filter(user=user)

ChartEditFormSet = modelformset_factory(
  ChartTable, 
  form=ChartEditForm,
  extra=0
)

