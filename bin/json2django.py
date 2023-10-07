#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-10-06 23:30:26

import sys
import os
import glob
import json
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
データベースに経済カレンダーの情報を追加する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("--encoding", metavar="encoding", default="utf-8", help="encoding")
  parser.add_argument("-u", "--username", metavar="username", help="username")
  # parser.add_argument("-", "--", action="store_true", help="")
  parser.add_argument("file", metavar="input-file", help="json file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  if not opsions.username:
    if "y" != input("usernameが指定されていませんが構いませんか？(y/other):")
      sys.exit()
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ExchangeProject.settings")
  import django
  django.setup()
  from django.conf import settings
  from diary.models import EventTable
  from accounts.models import CustomUser
  user = CustomUser.objects.get(username=options.username)
  data = json.load(open(options.file, mode="r", encoding=options.encoding))
  print(data)
  for d in data:
    if d["importance"] < 2:
      continue
    date = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()
    if d["time"] != "":
      time = datetime.datetime.strptime(d["time"], "%H:%M").time()
    else:
      time = None
    EventTable.objects.update_or_create(
      user = user,
      name = d["name"],
      country = d["country"],
      date = date,
      time = time,
      defaults = {
        "importance" : d["importance"],
        "previous" : d["previous"],
        "prediction" : d["prediction"],
        "result" : d["result"]
      }
    )

if __name__ == '__main__':
  main()
