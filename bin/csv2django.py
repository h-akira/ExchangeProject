#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-10-06 23:30:26

import sys
import os
import datetime
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-s", "--start", metavar="日付", help="2023-10-06などの形式の日付（Noneなら7日前")
  parser.add_argument("-p", "--pairs", metavar="pair", nargs="*", default=["USDJPY","EURJPY","EURUSD","GBPJPY", "AUDJPY"], help="通貨ペア")
  # parser.add_argument("-", "--", action="store_true", help="")
  # parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ExchangeProject.settings")
  import django
  django.setup()
  from django.conf import settings
  from api.models import ExchangeDataTable
  import FX
  now = datetime.datetime.now()-datetime.timedelta(hours=6)
  if options.start == None:
    options.start = now - datetime.timedelta(days=7)
  else:
    options.start = datetime.datetime.strptime(options.start, "%Y-%m-%d")
  date_range = (options.start.date(), (now + datetime.timedelta(days=1)).date())
  pair="USDJPY"
  for pair in options.pairs:
    df = FX.chart.GMO_dir2DataFrame(
      os.path.join(settings.BASE_DIR, "data/rate"), 
      pair=pair,
      date_range=date_range
    ) 
    # dict_list = [row.to_dict() for index, row in df.iterrows()]
    dict_list = [{'dt': index, **row.to_dict()} for index, row in df.iterrows()]
    for d in dict_list:
      d["pair"]=pair
      obj = ExchangeDataTable(**d)
      try:
        obj.save()
        if d["dt"].hour == 7 and d["dt"].minute == 0:
          print(f"{d['dt'].date()}の{d['pair']}を保存しました．")
      except django.db.utils.IntegrityError:
        if d["dt"].hour == 7 and d["dt"].minute == 0:
          print(f"{d['dt'].date()}の{d['pair']}は既に存在します．")


if __name__ == '__main__':
  main()
