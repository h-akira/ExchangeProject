import os
import sys
import datetime
import pandas as pd
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# 独自関数
import FX.chart

# @login_required
def get_data_by_date(request, date, pair, rule):
  date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
  if "H" in rule:
    days = 60
  elif "D" in rule:
    days = 250
  else:
    days = 10
  date_range = (
    date - datetime.timedelta(days=days),
    date + datetime.timedelta(days=1),
  )
  data = get_dic(pair, rule, date_range)
  return JsonResponse(data, safe=False)

##############################
########## Function ##########
##############################
def get_dic(pair, rule, date_range, sma1=5, sma2=20, sma3=60, end_datetime=None):
  df = FX.chart.GMO_dir2DataFrame(
    os.path.join(os.path.dirname(__file__), "../data/rate"), 
    pair=pair,
    date_range=date_range
  ) 
  if end_datetime != None:
    df = df[df.index <= end_datetime]
  df = FX.chart.resample(df, rule)
  df = FX.chart.add_BBands(
    df,20,2,0,name={"up":"bb_up_2", "middle":"bb_middle", "down":"bb_down_2"}
  )
  df = FX.chart.add_BBands(
    df,20,3,0,name={"up":"bb_up_3", "middle":"bb_middle", "down":"bb_down_3"}
  )
  df = FX.chart.add_SMA(df, sma1, "SMA1")
  df = FX.chart.add_SMA(df, sma2, "SMA2") 
  df = FX.chart.add_SMA(df, sma3, "SMA3")
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
