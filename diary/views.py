from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import datetime
from .models import EventTable, DiaryTable
from .forms import DiaryForm

# GPT先生に考えてもらった色
COLOR = {
  "Japan": "#BC002D",      # 日本の国旗の赤を使用: 鮮やかな赤色
  "EU": "#0000FF",         # 青: EUの旗の基調となる色
  "USA": "#B22234",        # アメリカの国旗の赤を使用: やや深めの赤色
  "Germany": "#FFCC00",    # ドイツの国旗の黄色を使用: 鮮やかな黄色
  "UK": "#C60C30",         # イギリスの国旗の赤を使用: やや深めの赤色
  "France": "#0055A4",     # フランスの国旗の青を使用: やや濃い青色
  "Canada": "#FF0000",     # カナダの国旗の赤を使用: 鮮やかな赤色
  "Australia": "#1F2F57",  # オーストラリアの国旗の青を使用: 深い青色
  "NewZealand": "#D52B1E", # ニュージーランドの国旗の赤を使用: 鮮やかな赤色
  "Swiss": "#D52B1E",      # スイスの国旗の赤を使用: 鮮やかな赤色
  "Turkey": "#E30A17",     # トルコの国旗の赤を使用: やや明るい赤色
  "China": "#DE2910",      # 中国の国旗の赤を使用: 鮮やかな赤色
  "Mexico": "#007748",     # メキシコの国旗の緑を使用: 深い緑色
  "Other": "#808080",      # グレー: 他のカテゴリを示すニュートラルな色
}
WEEK = ("月","火","水","木","金","土","日")

class IndexView(generic.TemplateView):
  template_name = 'diary/index.html'

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
  context = {
    "obj":obj,
    "str_date":str_date,
    "str_prev_date":str_prev_date,
    "str_next_date":str_next_date,
    "str_weekday":WEEK[date.weekday()],
    "option":option,
    "form":None,
    "type":None
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
  return redirect("diary:index")

def events_json(request):
  if request.user.is_authenticated:
    events = EventTable.objects.filter(Q(user=request.user) | Q(user=None))
  else:
    events = EventTable.objects.filter(user=None)
  event_list = [
    {
      'id': e.id,
      'title': e.title,
      'start': e.dt.strftime('%Y-%m-%dT%H:%M:%S'),
      'description': e.description,
      'borderColor': COLOR[e.country]
    }
    for e in events
  ]
  return JsonResponse(event_list, safe=False)
