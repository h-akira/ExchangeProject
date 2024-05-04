from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import ChartTable, CategoryTable,LinkTable
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request, category_number=1):
  categories = CategoryTable.objects.filter(user=request.user)
  if category_number != 1:
    if category_number > categories.count():
      return redirect('chart:index')
  if categories.exists():
    for i, category in enumerate(categories):
      if i == category_number:
        charts = ChartTable.objects.filter(category=category)
  context = {
    'categories': categories,
    'category_number': category_number,
  }
  return render(request, 'chart/index.html', context)

# ここからCategory
class CategoryCreateView(LoginRequiredMixin, CreateView):
  model = CategoryTable
  fields = ('name','description')
  template_name = 'chart/category_edit.html'
  success_url = reverse_lazy('chart:index')
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(CategoryCreateView, self).form_valid(form)
  def get_context_data(self):
    context = super().get_context_data()
    context["edit_type"] = "create"
    return context

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
  model = CategoryTable
  fields = ('name','description')
  template_name = 'chart/category_edit.html'
  success_url = reverse_lazy('chart:index')
  def get_context_data(self):
    context = super().get_context_data()
    context["edit_type"] = "update"
    return context

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
  model = CategoryTable
  template_name = 'chart/category_delete.html'
  success_url = reverse_lazy('chart:index')

# ここからchart
# class ChartCreateView(LoginRequiredMixin, CreateView):
#   model = CategoryTable
#   fields = ('name','discription')
#   template_name = 'chart/category_edit.html'
#   success_url = reverse_lazy('chart:index')
#   def form_valid(self, form):
#     form.instance.user = self.request.user
#     return super(CategoryCreateView, self).form_valid(form)
#   def get_context_data(self):
#     context = super().get_context_data()
#     context["edit_type"] = "create"
#     return context
#
# class CategoryUpdateView(LoginRequiredMixin, UpdateView):
#   model = CategoryTable
#   fields = ('name','discription')
#   template_name = 'chart/category_edit.html'
#   success_url = reverse_lazy('chart:index')
#   def get_context_data(self):
#     context = super().get_context_data()
#     context["edit_type"] = "update"
#     return context
#
# class CategoryDeleteView(LoginRequiredMixin, DeleteView):
#   model = CategoryTable
#   template_name = 'chart/category_delete.html'
#   success_url = reverse_lazy('chart:index')
#
#
