from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
import datetime
from .models import EventTable, DiaryTable
from .forms import DiaryForm
from api.models import ExchangeDataTable

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
dic = {
  "Japan": "日",
  "EU": "欧",
  "USA": "米",
  "Germany": "独",
  "UK": "英",
  "France": "仏",
  "Canada": "加",
  "Australia": "豪",
  "NewZealand": "新",
  "Swiss": "瑞",
  "Turkey": "土",
  "China": "中",
  "Mexico": "墨",
  "Other": "他"
}
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
  # 為替データの最終時刻を取得し，当日のデータがあるのかどうか判断する
  # UTCで返される
  latest_date = ExchangeDataTable.objects.aggregate(max_dt=Max('dt'))['max_dt'].date()
  if latest_date < date:
    is_data=False
  else:
    is_data=True
  print(is_data)
  context = {
    "obj":obj,
    "str_date":str_date,
    "str_prev_date":str_prev_date,
    "str_next_date":str_next_date,
    "str_weekday":WEEK[date.weekday()],
    "option":option,
    "form":None,
    "type":None,
    "is_data":is_data
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

def events_json(request):
  if request.user.is_authenticated:
    events = EventTable.objects.filter(Q(user=request.user) | Q(user=None))
  else:
    events = EventTable.objects.filter(user=None)
  event_list = []
  for e in events:
    if e.time:
      start = datetime.datetime.combine(e.date, e.time).strftime('%Y-%m-%dT%H:%M:%S')
      # デフォルトでendがstartの一時間後になるようで，日付をまたぐことがあるので
      end = (datetime.datetime.combine(e.date, e.time)+datetime.timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S')
    else:
      start = e.date.strftime('%Y-%m-%d')
      end = start
    event_list.append(
      {
        'id': e.id,
        'title': f"【{dic[e.country]}{e.importance}】{e.name}",
        'start':start,
        'end':end, 
        'description': e.description,
        'borderColor': COLOR[e.country],
        'backgroundColor': COLOR[e.country]
      }
    )
  return JsonResponse(event_list, safe=False)


