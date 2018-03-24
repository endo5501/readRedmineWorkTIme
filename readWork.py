#_ -*- coding: utf-8 -*-

import datetime
from redminelib import Redmine

redmine = Redmine('http://localhost/redmine', key='6a2dd636ad3ee03f9f3d7d9fbb93346de3f32add')

time_entries = redmine.time_entry.all()


issue_table={}
spent_list=[]

base = datetime.date(2018,3,1)
for i in range(0,30):
  d = base + datetime.timedelta(i)
  spent_list.append(d)


for t in time_entries:
  #print('issue_id:{0},spend_on:{1},hours:{2},activity_id:{3}'.format(t.issue,t.spent_on,t.hours,t.activity))
  act_table={}
  spent_table={}
  hours = 0
  #spent_list作成
  #if not t.spent_on in spent_list:
  #  spent_list.append(t.spent_on)
  #issue_tableデータ構造作成
  if t.issue.id in issue_table:
    act_table = issue_table[t.issue.id]
  if t.activity.id in act_table:
    spent_table = act_table[t.activity.id]
  if t.spent_on in spent_table:
    hours = spent_table[t.spent_on]
  spent_table[t.spent_on] = hours + t.hours
  act_table[t.activity.id] = spent_table
  issue_table[t.issue.id] = act_table

#print(issue_table)
#for issue,act_table in issue_table.items():
#  print(issue)
#  for act,spent_table in act_table.items():
#    print('\t{0}'.format(act))
#    for spent,hour in spent_table.items():
#      print('\t\t{0}'.format(spent))
#      print('\t\t{0}'.format(hour))

print('issue,',end="")
for issue,act_table in issue_table.items():
  act_num = len(act_table)
  print('{0}'.format(issue),end="")
  for i in range(8,13):
    print(',',end="")
print("")

print('activity,',end="")
#for issue,act_table in issue_table.items():
#  for act,spent_table in act_table.items():
#    print('{0},'.format(act),end="")
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
      #if a in act_table:
        #spent_table = act_table[a]
        
        #  print('{0},'.format(
    #for act,spent_table in act_table.items():
    #  for spent,hour in spent_table.items():
    #    if spent==s:
    #      print('{0},'.format(hour),end="")
    #    else:
    #      print('0,',end="")
  print("")
