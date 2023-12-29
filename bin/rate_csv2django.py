#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-10-06 23:30:26

import sys
import os
import glob
import re
import datetime
from pytz import timezone
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.chart import chart

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
データベースに為替のデータを登録する．\
GMOクリック証券のヒストリカルデータを利用することを想定している．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-i", "--input", metavar="directry", help="rateディレクトリ（NoneならBASE_DIR/data/rate）")
  parser.add_argument("-s", "--start", metavar="日付", help="2023-10-06などの形式の日付（Noneなら現在の50日前）")
  parser.add_argument("-p", "--pairs", metavar="pair", nargs="*", default=[
"USDJPY",
"EURJPY",
"EURUSD",
"GBPJPY",
"AUDJPY",
"GBPUSD",
"AUDUSD"
], help="通貨ペア")
  parser.add_argument("-r", "--rule", metavar="rule", default="15T", help="時間足")
  # parser.add_argument("-", "--", action="store_true", help="")
  # parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def GMO_dir2DataFrame(dir_name,pair="USDJPY",date_range=None, BID_ASK="BID"):
  # pairは"/"を含んでいてもいなくても処理可能
  # date_rangeはdatetime.date型を要素に持つリストまたはタプル
  # ディレクトリ構造は以下の通り:
  # .
  # |-USDJPY
  # | |-202303
  # | | |-USDJPY_20230301.csv
  # | | |-USDJPY_20230302.csv
  # | | |-USDJPY_20230303.csv
  # | | |-...
  # | |-202304
  # | | |-...
  # | |-202305
  # |   |-...
  # |-EURJPY
  #    |-...
  file_list = glob.glob(os.path.join(dir_name,pair.replace("/",""))+f"/*/{pair.replace('/','')}_*.csv")
  df = pd.DataFrame()
  for file in file_list:
    if os.path.basename(file)[:len(pair.replace("/",""))] != pair.replace("/","") or file[-4:] != ".csv":
      print(f"skip: {file}")
      continue
    m = re.search(r"\d{4}\d{2}\d{2}", file)
    if m:
      file_date = datetime.datetime.strptime(m.group(),"%Y%m%d").date()  # 日付文字列を取得
    else:
      continue
    if date_range != None:
      if date_range[0] <= file_date < date_range[1]:
        pass
      else:
        continue
    df = pd.concat([df,GMO_csv2DataFrame(file,BID_ASK=BID_ASK)])
  if len(df) == 0:
    print(dir_name, pair, date_range)
    raise Exception("No Data")
  df = df.sort_values(by="date", ascending=True)
  return df

def GMO_csv2DataFrame(file_name,BID_ASK="BID"):
  # GMOクリック証券からダウンロードしたヒストリカルデータ（CSVファイル）を読み込み，
  # mplfinanceで扱えるデータフレームにして返す．
  if not os.path.isfile(file_name):
    raise FileNotFoundError(f"{file_name}は存在しません．")
  df = pd.read_csv(file_name, encoding='shift_jis').rename(
    columns={
      '日時':'date', 
      f'始値({BID_ASK})':'Open', 
      f'高値({BID_ASK})':'High', 
      f'安値({BID_ASK})':'Low', 
      f'終値({BID_ASK})':'Close'
    }
  )
  for col in df:
    if col not in ["Open", "High", "Low", "Close", "date"]:
      df = df.drop(col, axis=1) 
  df["date"] = pd.to_datetime(df["date"])
  df.set_index("date", inplace=True)
  df.index = df.index.tz_localize(timezone('Asia/Tokyo'))
  return df

def main():
  options = parse_args()
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ExchangeProject.settings")
  import django
  django.setup()
  from django.conf import settings
  from api.models import ExchangeDataTable
  now = datetime.datetime.now()-datetime.timedelta(hours=6)
  if options.start == None:
    options.start = now - datetime.timedelta(days=50)
  else:
    options.start = datetime.datetime.strptime(options.start, "%Y-%m-%d")
  date_range = (options.start.date(), (now + datetime.timedelta(days=1)).date())
  if not options.input:
    options.input = os.path.join(settings.BASE_DIR, "data/rate") 
  for pair in options.pairs:
    df = GMO_dir2DataFrame(
      dir_name=options.input,
      pair=pair,
      date_range=date_range
    ) 
    df = chart.resample(df, rule=options.rule)
    dict_list = [{'dt': index, **row.to_dict()} for index, row in df.iterrows()]
    obj_list = []
    for d in dict_list:
      d["pair"]=pair
      obj = ExchangeDataTable(**d)
      obj_list.append(obj)
      # try:
      #   obj.save()
      #   if d["dt"].hour == 7 and d["dt"].minute == 0:
      #     print(f"{d['dt'].date()}の{d['pair']}を保存しました．")
      # except django.db.utils.IntegrityError:
      #   if d["dt"].hour == 7 and d["dt"].minute == 0:
      #     print(f"{d['dt'].date()}の{d['pair']}は既に存在します．")
    ExchangeDataTable.objects.bulk_create(obj_list, ignore_conflicts=True)

if __name__ == '__main__':
  main()
