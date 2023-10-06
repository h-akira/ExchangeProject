import os
import sys
import datetime
import pytz
import pandas as pd
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ExchangeDataTable
# 独自関数
import chart.chart

# @login_required
def get_data_by_date(request, date, pair, rule):
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  end_datetime = datetime.datetime.combine(date, datetime.time(21,0))
  end_datetime = pytz.utc.localize(end_datetime)
  if "H" in rule:
    days = 60
  elif "D" in rule:
    days = 250
  else:
    days = 10
  start_datetime = end_datetime - datetime.timedelta(days=days)
  data = get_dic(pair, rule, start_datetime=start_datetime, end_datetime=end_datetime)
  return JsonResponse(data, safe=False)

##############################
########## Function ##########
##############################
def get_dic(pair, rule, sma1=5, sma2=20, sma3=60, start_datetime=None, end_datetime=None):
  if start_datetime == None and end_datetime == None:
    Rate = ExchangeDataTable.objects.filter(pair=pair)
  elif start_datetime == None:
    Rate = ExchangeDataTable.objects.filter(pair=pair, dt__lt=end_datetime)
  elif end_datetime == None:
    Rate = ExchangeDataTable.objects.filter(pair=pair, dt__gte=start_datetime)
  else:
    Rate = ExchangeDataTable.objects.filter(pair=pair, dt__gte=start_datetime, dt__lt=end_datetime)
  Rate = Rate.order_by("dt")
  df = pd.DataFrame.from_records(Rate.values())
  df['dt'] = pd.to_datetime(df['dt'])
  df['dt'] = df['dt'].dt.tz_convert('Asia/Tokyo')
  df = df.drop(columns=['id', 'pair'])
  df.set_index('dt', inplace=True)
  df = chart.chart.resample(df, rule)
  df = chart.chart.add_BBands(
    df,20,2,0,name={"up":"bb_up_2", "middle":"bb_middle", "down":"bb_down_2"}
  )
  df = chart.chart.add_BBands(
    df,20,3,0,name={"up":"bb_up_3", "middle":"bb_middle", "down":"bb_down_3"}
  )
  df = chart.chart.add_SMA(df, sma1, "SMA1")
  df = chart.chart.add_SMA(df, sma2, "SMA2") 
  df = chart.chart.add_SMA(df, sma3, "SMA3")
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
  return data
