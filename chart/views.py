from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChartTable, CategoryTable,LinkTable

@login_required
def index(request, category_number=0):
  categorys = CategoryTable.objects.filter(user=request.user)
  if category_number != 0:
    if category_number <= categorys.count()-1:
      redirect('chart:index')
  # now_open = []
  if categorys.exists():
    for i, category in enumerate(categorys):
      if i == category_number:
        charts = ChartTable.objects.filter(category=category)
  context = {
    'categorys': categorys,
    'category_number': category_number,
  }
  return render(request, 'chart/index.html')
