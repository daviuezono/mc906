#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
from os import system
from random import shuffle

################### parameters/constants  ####################
MIN_GENS = 15
ROOMS = 1
CLASSES = 80
CL_DAYS = 5 # mon, tue, wed, thu, fri
CL_HOURS = 6 # 8, 10, 14, 16, 19, 21
UNAVAILABLE = 0
AVAILABLE = 1
PREFERENTIAL = 2

######################### functions  #########################
def bitwise(one, two):
  out = []
  for i in range(CL_DAYS+CL_HOURS):
    el_one = int(one[i])
    el_two = int(two[i])
    el_bit = bool(el_one) & bool(el_two)
    if not el_bit:
      out.append(0)
    else:
      out.append(el_one)

  days_of_week = out[0 : CL_DAYS]
  hours_of_day = out[CL_HOURS-1 : ]

  if   (days_of_week.count(PREFERENTIAL) == 1) and (hours_of_day.count(PREFERENTIAL) == 1):
    return 3, days_of_week.index(PREFERENTIAL), hours_of_day.count(PREFERENTIAL)
  elif (days_of_week.count(PREFERENTIAL) == 1) and (hours_of_day.count(AVAILABLE) == 1):
    return 2, days_of_week.index(PREFERENTIAL), hours_of_day.count(AVAILABLE)
  elif (days_of_week.count(AVAILABLE) == 1) and (hours_of_day.count(PREFERENTIAL) == 1):
    return 2, days_of_week.index(AVAILABLE), hours_of_day.count(PREFERENTIAL)
  elif (days_of_week.count(AVAILABLE) == 1) and (hours_of_day.count(AVAILABLE) == 1):
    return 1, days_of_week.index(AVAILABLE), hours_of_day.count(AVAILABLE)
  else:
    return 0, UNAVAILABLE, UNAVAILABLE

def shuffle_elements(values):
  days_of_week = values[0 : CL_DAYS]
  shuffle(days_of_week)
  hours_of_day = values[CL_HOURS-1 : ]
  shuffle(hours_of_day)
  
  string = ''
  for i in range(len(days_of_week)):
    if i:
      string += ' '
    string += days_of_week[i]
  for i in range(len(hours_of_day)):
    string += ' '
    string += hours_of_day[i]
  string += "\n"
  return string

################ checking folder structure ###################
check_folder = "ls -l | grep genxx | wc -l"
has_folder = int(subprocess.check_output(check_folder, shell=True))
if not has_folder:
  create_folder = "mkdir genxx"
  system(create_folder)
copy_initial = "cp input genxx/gen00"
system(copy_initial)

######## allocation: a linear vector for schedule ############
# allocation[0] is Monday 8, allocation[1] is Monday 10, ..., 
# allocation[7] is Tuesday 10, and so on.
# allocation[x*CL_DAYS+y] represents day x at hour y
# x from 0 (mon) to 4 (fri); y from 0 (8h) to 5 (21h)
# it starts with 0 (zero) and is increased up to ROOMS
allocation = []
for i in range(CL_DAYS*CL_HOURS):
  allocation.append(0)


######################## MAIN MAIN MAIN ##########################
######################## MAIN MAIN MAIN ##########################

print "\n"
print "SCORES"
print "------"
will_have_next_gen = 1
curr_gen = 0
scores = []
while will_have_next_gen:

  curr_score = 0
  prefs = open("prefs", "r")
  curr = open("genxx/gen" + str(curr_gen).zfill(2), "r")
  next = open("genxx/gen" + str(curr_gen+1).zfill(2), "w")

  for i in range(CLASSES):
    pref_line = prefs.readline()
    pref_values = pref_line.split()
    curr_line = curr.readline()
    curr_values = curr_line.split()
    #print "[DEBUG] gen" + str(curr_gen).zfill(2) + " @ line " + str(i).zfill(2)
    result, day, hour = bitwise(pref_values, curr_values)
    if bool(result) and (allocation[day*CL_DAYS+hour] < ROOMS):
      curr_score += result
      allocation[day*CL_DAYS+hour] += 1
      next.write(curr_line)
    else:
      next_line = shuffle_elements(curr_values)
      next.write(next_line)

  if (curr_gen >= MIN_GENS) and (curr_score == scores[-1]) and (curr_score == scores[-2]):
    will_have_next_gen = 0

  scores.append(curr_score)
  print "gen" + str(curr_gen).zfill(2) + ": " + str(scores[curr_gen])

  curr_gen += 1
  curr_score = 0

  prefs.close()
  curr.close()
  next.close()

print "\n"
