#_ -*- coding: utf-8 -*-
import sys
import datetime
import calendar
import argparse
from redminelib import Redmine

#引数読み取り
parser = argparse.ArgumentParser(description='Redmineから工数情報を読み取り、csv形式で一月の結果を出力します')
parser.add_argument('URL', help='RedmineのURL')
parser.add_argument('API_KEY', help='RedmineのAPI key')
parser.add_argument('--user_id',type=int, help='ユーザID(デフォルト:自分)')
parser.add_argument('--date', help='出力する年/月(例:2018/03,デフォルト:今月)')
args = parser.parse_args()

#redmine接続
redmine = Redmine(args.URL, key=args.API_KEY)

#対象ユーザ
if args.user_id==None:
  user = redmine.user.get('current')
  user_id = user.id
else:
  user_id = args.user_id

#集計期間
spent_list=[]
if args.date==None:
  from_date = datetime.date.today().replace(day=1)
else:
  tmp_date = datetime.datetime.strptime(args.date,'%Y/%m')
  from_date = datetime.date(tmp_date.year,tmp_date.month,tmp_date.day)

max_day = calendar.monthrange(from_date.year,from_date.month)[1]
to_date = from_date + datetime.timedelta(max_day-1)

print(from_date)
print(to_date)

for d in range(max_day):
  spent_list.append(from_date + datetime.timedelta(d))

#工数データ取得
issue_table={}
time_entries = redmine.time_entry.filter(user_id = user_id, fome_date = from_date, to_date = to_date)

for t in time_entries:
  act_table={}
  spent_table={}
  hours = 0
  
  issue = redmine.issue.get(t.issue.id)
  main_key = "#" + str(t.issue.id)
  for c in issue.custom_fields:
    if c.id == 1 and c.value != '':
      main_key = "E"+c.value
  if main_key in issue_table:
    act_table = issue_table[main_key]
  if t.activity.id in act_table:
    spent_table = act_table[t.activity.id]
  if t.spent_on in spent_table:
    hours = spent_table[t.spent_on]
  spent_table[t.spent_on] = hours + t.hours
  act_table[t.activity.id] = spent_table
  issue_table[main_key] = act_table

print(issue_table)
for issue,act_table in issue_table.items():
  print(issue)
  for act,spent_table in act_table.items():
    print('\t{0}'.format(act))
    for spent,hour in spent_table.items():
      print('\t\t{0}'.format(spent))
      print('\t\t{0}'.format(hour))


#CSV出力
print('issue,',end="")
for issue,act_table in issue_table.items():
  act_num = len(act_table)
  print('{0}'.format(issue),end="")
  for i in range(8,13):
    print(',',end="")
print("")

print('activity,',end="")
for issue,act_table in issue_table.items():
  for i in range(8,13):
    print('{0},'.format(i),end="")
print("")

spent_list.sort()
for s in spent_list:
  print('{0},'.format(s),end="")
  for issue,act_table in issue_table.items():
    for a in range(8,13):
      if a in act_table:
        spent_table = act_table[a]
        if s in spent_table:
          print('{0},'.format(spent_table[s]),end="")
        else:
          print('0,',end="")
      else:
        print('0,',end="")
  print("")
