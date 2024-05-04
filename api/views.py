import os
import sys
import datetime
import pytz
import pandas as pd
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ExchangeDataTable, EventTable, dic_omit
from django.db.models import Q, Max, Min
import pandas_datareader.data as web
import yfinance as yf
yf.pdr_override()
from ExchangePackage import chart


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
    if e.importance:
      title = f"【{dic_omit[e.country]}{e.importance}】{e.name}"
    else:
      title = f"【{dic_omit[e.country]}】{e.name}"
    event_list.append(
      {
        'id': e.id,
        'title': title,
        'start':start,
        'end':end, 
        'borderColor': COLOR[e.country],
        'backgroundColor': COLOR[e.country]
      }
    )
  return JsonResponse(event_list, safe=False)

# @login_required
def get_data_by_date(request, date, pair, rule):
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  end_datetime = datetime.datetime.combine(date, datetime.time(21,0))
  end_datetime = pytz.utc.localize(end_datetime)
  if "D" in rule:
    days = 250
  elif "H" in rule:
    days = 60
  elif rule in ["15T", "30T"]:
    days = 21
  else:
    # yfinanceの制約で1分足は7日分しか取得できない
    # yfinanceの制約で10分足等は取得できず1分足から変換する
    days = 7
  start_datetime = end_datetime - datetime.timedelta(days=days)
  data = _get_dic(pair, rule, start_datetime=start_datetime, end_datetime=end_datetime)
  return JsonResponse(data, safe=False)

def get_data_by_event(request, event_id, pair, rule):
  event = EventTable.objects.get(id=event_id)
  if not event.time and event.time != datetime.time(0,0):
    return JsonResponse({}, safe=False)
  dt = datetime.datetime.combine(event.date, event.time)
  dt = pytz.timezone("Asia/Tokyo").localize(dt)
  if "T" in rule:
    m = int(rule.replace("T", ""))
  elif "H" in rule:
    m = int(rule.replace("H", "")) * 60
  else:
    return JsonResponse({}, safe=False)
  start_datetime = dt - datetime.timedelta(minutes=m*200)
  end_datetime = dt + datetime.timedelta(minutes=m*80)
  data = _get_dic(pair, rule, start_datetime=start_datetime, end_datetime=end_datetime)
  return JsonResponse(data, safe=False)

def get_latest_data_by_yf(request, pair, rule):
  # date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  # end_datetime = datetime.datetime.combine(date, datetime.time(21,0))
  end_datetime = datetime.datetime.utcnow()
  end_datetime = pytz.utc.localize(end_datetime)
  if "D" in rule:
    days = 250
  elif "H" in rule:
    days = 60
  elif rule in ["15T", "30T"]:
    days = 21
  else:
    # yfinanceの制約で1分足は7日分しか取得できない
    # yfinanceの制約で10分足等は取得できず1分足から変換する
    days = 7
  start_datetime = end_datetime - datetime.timedelta(days=days)
  data = _get_dic(pair, rule, start_datetime=start_datetime, end_datetime=end_datetime, yf_must=True)
  return JsonResponse(data, safe=False)

##############################
########## Function ##########
##############################
def _get_dic(pair, rule, sma1=9, sma2=20, sma3=60, start_datetime=None, end_datetime=None, yf_must=False):
  # データベースにデータがあるかどうか確認，なければyfinanceから取得
  # 期間が指定されていない場合はyfinanceを使わず無条件でデータベースにあるものすべてを取得
  if "T" in rule:
    m = int(rule.replace("T", ""))
  else:
    m = 1500  # 適当な数字
  if yf_must:
    yf = True
  else:
    dataObjects = ExchangeDataTable.objects.filter(pair=pair.replace("/","")).order_by("dt")
    if m < 15 or m%15 != 0:
      yf = True
    elif dataObjects.count() == 0:
      yf=True
    elif start_datetime == None or end_datetime == None:
      yf=False
    else:
      latest_result = dataObjects.aggregate(max_dt=Max('dt'))
      latest_date = latest_result['max_dt'].date() if latest_result['max_dt'] else None
      oldest_result = dataObjects.aggregate(min_dt=Min('dt'))
      oldest_date = oldest_result['min_dt'].date() if oldest_result['min_dt'] else None
      if latest_date == None or oldest_date == None:
        yf=True
      elif latest_date < end_datetime.date() or oldest_date > start_datetime.date():
        yf=True
      else:
        yf=False
  if yf:
    print("get data from yfinance")
    # intervalは1, 2, 5, 15, 30, 60, 1h, 1d, 1wk, 1mo, 3moに対応するらしい
    interval = rule.replace("T", "m").replace("H", "h").replace("D", "d")
    if interval not in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d"]:
      resample = True
      interval = str(1)+interval[-1]
    else:
      resample = False
    if "^" in pair:
      ticker = pair
    else:
      ticker = f'{pair.replace("/","")}=X'
    df = web.get_data_yahoo(tickers=ticker,start=start_datetime, end=end_datetime, interval=interval)
    # if df.empty:
      # return {"source": "Failed download by yahoo finance", "data": []}
    if df.index[0].tzinfo is None:
      df.index = df.index.tz_localize('UTC')
    df.index = df.index.tz_convert('Asia/Tokyo')
    if resample:
      df = chart.resample(df, rule)
  else:
    print("get data from database")
    if start_datetime == None and end_datetime == None:
      Rate = dataObjects
    elif start_datetime == None:
      Rate = dataObjects.filter(dt__lt=end_datetime)
    elif end_datetime == None:
      Rate = dataObjects.filter(dt__gte=start_datetime)
    else:
      Rate = dataObjects.filter(dt__gte=start_datetime, dt__lt=end_datetime)
    Rate = Rate.order_by("dt")
    df = pd.DataFrame.from_records(Rate.values())
    df['dt'] = pd.to_datetime(df['dt'])
    df['dt'] = df['dt'].dt.tz_convert('Asia/Tokyo')
    df = df.drop(columns=['id', 'pair'])
    df.set_index('dt', inplace=True)
    df = chart.resample(df, rule)
  df = chart.add_BBands(
    df,20,2,0,name={"up":"bb_up_2", "middle":"bb_middle", "down":"bb_down_2"}
  )
  df = chart.add_BBands(
    df,20,3,0,name={"up":"bb_up_3", "middle":"bb_middle", "down":"bb_down_3"}
  )
  df = chart.add_SMA(df, sma1, "SMA1")
  df = chart.add_SMA(df, sma2, "SMA2") 
  df = chart.add_SMA(df, sma3, "SMA3")
  df = df.dropna() 
  data = []
  for index, row in df.iterrows():
    data.append(
      {
        "time": int(index.tz_localize(None).timestamp()),
        "open": row["Open"],
        "high": row["High"],
        "low": row["Low"],
        "close": row["Close"],
        "sma1": row["SMA1"],
        "sma2": row["SMA2"],
        "sma3": row["SMA3"],
        "bb_up_2": row["bb_up_2"],
        "bb_up_3": row["bb_up_3"],
        "bb_down_2": row["bb_down_2"],
        "bb_down_3": row["bb_down_3"]
      }
    )
  if yf:
    source = "Yahoo Finance"
  else:
    source = "My Database"
  return {
    "source": source,
    "data": data
  }
