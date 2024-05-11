from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import ChartTable, CategoryTable,LinkTable
from .forms import ChartEditForm, ChartEditFormSet
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max

@login_required
def index(request, category_number=1):
  categories = CategoryTable.objects.filter(user=request.user)
  if category_number != 1:
    if category_number > categories.aggregate(Max('id'))['id__max']:
      return redirect('chart:index')
  if categories.exists():
    for category in categories:
      if category.id == category_number:
        charts = ChartTable.objects.filter(category=category).order_by('-priority')
        break
    else:
      raise Exception
  else:
    charts = None
  context = {
    'categories': categories,
    'category_number': category_number,
    'charts': charts,
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

class ChartCreateView(LoginRequiredMixin, CreateView):
  model = ChartTable
  form_class = ChartEditForm
  # fields = ('name','source',"symbol","category")
  template_name = 'chart/chart_edit.html'
  success_url = reverse_lazy('chart:index')
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(ChartCreateView, self).form_valid(form)
  def get_context_data(self):
    context = super().get_context_data()
    context["edit_type"] = "create"
    return context
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

class ChartDeleteView(LoginRequiredMixin, DeleteView):
  model = ChartTable
  template_name = 'chart/chart_delete.html'
  success_url = reverse_lazy('chart:index')

# コピっただけ
@login_required
def chart_settings(request,category_id):
  category = CategoryTable.objects.get(id=category_id)
  if category.user != request.user:
    return redirect('chart:index')
  charts = ChartTable.objects.filter(category=category)
  if request.method == "POST":
    # formset = ChartEditFormSet(request.POST, queryset=charts)
    formset = ChartEditFormSet(request.POST, queryset=charts, form_kwargs={'user': request.user})
    if formset.is_valid():
      formset.save()
      if request.POST['action'] == 'continue':
        return redirect("chart:chart_settings", category_id)
      elif request.POST['action'] == 'end':
        return redirect("chart:category", category_id)
      else:
        raise Exception
    else:
      print("---- Error ----")
      print("formset.errors:")
      print(formset.errors)
      print("formset.management_form.erros:")
      print(formset.management_form.errors)
      print("---------------")
      raise Exception
  else:
    print(len(charts))
    charts = ChartTable.objects.filter(category=category)
    # formset = ChartEditFormSet(queryset=charts, user=request.user)  # ユーザー情報をフォームセットに渡す
    formset = ChartEditFormSet(queryset=charts, form_kwargs={'user': request.user})
    context = {
      "formset": formset,
      "charts": charts,
      "category": category,
    }
    return render(request, 'chart/chart_edit_set.html', context)

