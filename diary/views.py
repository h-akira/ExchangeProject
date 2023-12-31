from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.db.models import Q, Max, Min
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from .models import DiaryTable
from api.models import EventTable
from .forms import DiaryForm

WEEK = ("月","火","水","木","金","土","日")

class IndexView(LoginRequiredMixin, generic.TemplateView):
  template_name = 'diary/index.html'
  login_url = reverse_lazy("login")

@login_required
def detail(request,date,option=None):
  str_date = date
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  prev_date = date - datetime.timedelta(days=1)
  next_date = date + datetime.timedelta(days=1)
  str_next_date = next_date.strftime('%Y-%m-%d')
  str_prev_date = prev_date.strftime('%Y-%m-%d')
  try:
    obj = DiaryTable.objects.get(user=request.user, date=date)
  except DiaryTable.DoesNotExist:
    obj = None
  events_1 = EventTable.objects.filter(date=date, time__gte=datetime.time(6,0))
  events_2 = EventTable.objects.filter(date=date + datetime.timedelta(days=1), time__lt=datetime.time(6,0))
  events = events_1 | events_2
  events = events.order_by("date", "time")
  if (datetime.datetime.utcnow() - datetime.timedelta(hours=21)).date() < date:
    is_data=False  # 当日であればウィジェットを使う
  else:
    is_data=True  # 前日までならデータを用いてチャートを作成する
  if (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).date() < date:
    future = True  # 未来の日付であればチャートを表示しない
  else:
    future = False
  context = {
    "obj":obj,
    "str_date":str_date,
    "str_prev_date":str_prev_date,
    "str_next_date":str_next_date,
    "str_weekday":WEEK[date.weekday()],
    "option":option,
    "form":None,
    "type":None,
    "is_data":is_data,
    "future":future,
    "events":events,
  }
  if option == "edit":
    if obj == None:
      form = DiaryForm()
      context["type"] = "create"
    else:
      form = DiaryForm(instance=obj)
      context["type"] = "update"
    context["form"] = form
  return render(request, 'diary/diary.html', context)

@login_required
def create(request, date):
  str_date = date
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  if request.method == 'POST':
    form = DiaryForm(request.POST)
    if form.is_valid():
      instance = form.save(commit=False)  # まだDBには保存しない
      instance.date = date # 日付をセット
      instance.user = request.user  # userをセット
      instance.save()  # DBに保存
    return redirect("diary:detail", str_date)

@login_required
def update(request, date):
  str_date = date
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  obj = DiaryTable.objects.get(user=request.user, date=date)
  if request.method == 'POST':
    form = DiaryForm(request.POST, instance=obj)
    if form.is_valid():
      form.save()
    return redirect("diary:detail", str_date)

@login_required
def delete(request, date):
  str_date = date
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  obj = DiaryTable.objects.get(user=request.user, date=date)
  obj.delete()
  return redirect("diary:detail", str_date)

