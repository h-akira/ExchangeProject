#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-10-06 23:30:26

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
データベースのデータを一括削除する
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  # parser.add_argument("-", "--", action="store_true", help="")
  # parser.add_argument("file", metavar="input-file", help="json file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ExchangeProject.settings")
  import django
  django.setup()
  from django.conf import settings
  print("一括削除したいものを選択してください．")
  print("1: ExchangeDataTable")
  print("2: EventTable")
  choice = input(">> ")
  if choice == "1":
    if "y" == input("ExchangeDataTableを本当に削除しますか？(y/n) >> "):
      from api.models import ExchangeDataTable
      ExchangeDataTable.objects.all().delete()
      print("ExchangeDataTableを削除しました．")
  elif choice == "2":
    if "y" == input("EventTableを本当に削除しますか？(y/n) >> "):
      from api.models import EventTable
      EventTable.objects.all().delete()
      print("EventTableを削除しました．")
  else:
    print("選択肢にありません．")

if __name__ == '__main__':
  main()
