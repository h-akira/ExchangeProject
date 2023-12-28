from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from api.models import EventTable
from .models import EventCommentTable
from .forms import EventCommentForm
import datetime
import pytz

WEEK = ("月","火","水","木","金","土","日")

@login_required
def detail(request,id,option=None):
  # str_next_date = next_date.strftime('%Y-%m-%d')
  # str_prev_date = prev_date.strftime('%Y-%m-%d')
  event = EventTable.objects.get(id=id)
  str_date = event.date.strftime('%Y-%m-%d')
  try:
    comment = EventCommentTable.objects.get(event=event,user=request.user)
  except EventCommentTable.DoesNotExist:
    comment = None
  dt = datetime.datetime.combine(event.date, event.time)
  dt = pytz.timezone("Asia/Tokyo").localize(dt)
  # yahoo finance APIの仕様上，時間足によっては一定以上以前のデータを取得できないため対応
  # 60日以上前のデータは15分足のものを自前で用意していることを前提としている
  if datetime.datetime.now(datetime.timezone.utc) - dt > datetime.timedelta(days=60):
    min_interval = "15T"
  elif datetime.datetime.now(datetime.timezone.utc) - dt > datetime.timedelta(days=30):
    min_interval = "5T"
  else:
    min_interval = "1T"
  if event.time:
    is_data=True
  else:
    is_data=False 
  # if pytz.timezone("Asia/Tokyo").localize(datetime.datetime.now()) < dt:
  if datetime.datetime.now(datetime.timezone.utc) < dt:
    future = True  # 未来の日付であればチャートを表示しない
  else:
    future = False
  context = {
    "event":event,
    "comment":comment,
    "str_date":datetime.datetime.strftime(event.date,'%Y-%m-%d'),
    "str_weekday":WEEK[event.date.weekday()],
    "option":option,
    "form":None,
    "type":None,
    "min_interval":min_interval,
    "is_data":is_data,
    "future":future,
    "event":event,
  }
  if option == "edit":
    if comment == None:
      form = EventCommentForm()
      context["type"] = "create"
    else:
      form = EventCommentForm(instance=comment)
      context["type"] = "update"
    context["form"] = form
  return render(request, 'events/event.html', context)

@login_required
def create(request, id):
  event = EventTable.objects.get(id=id)
  if request.method == 'POST':
    form = EventCommentForm(request.POST)
    if form.is_valid():
      instance = form.save(commit=False)  # まだDBには保存しない
      instance.event = event  # eventをセット
      instance.user = request.user  # userをセット
      instance.save()  # DBに保存
    return redirect("events:detail", id)

@login_required
def update(request, id):
  event = EventTable.objects.get(id=id)
  comment = EventCommentTable.objects.get(event=event,user=request.user)
  if request.method == 'POST':
    form = EventCommentForm(request.POST, instance=comment)
    if form.is_valid():
      form.save()
    return redirect("events:detail", id)

@login_required
def delete(request, id):
  event = EventTable.objects.get(id=id)
  comment = EventCommentTable.objects.get(event=event,user=request.user)
  comment.delete()
  return redirect("events:detail", id)
