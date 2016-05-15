#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
from os import system
from random import shuffle
from sys import argv
from sys import exit

if len(argv) != 5:
  print "---> Usage: python main.py $CLASSES $MIN_GENS $ROOMS $RATIO"
  exit(0)

################### parameters/constants  ####################
CLASSES = int(argv[1])
MIN_GENS = int(argv[2])
ROOMS = int(argv[3])
RATIO = int(argv[4])
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

  days = out[0 : CL_DAYS]
  hours = out[CL_HOURS-1 : ]

  if   (days.count(PREFERENTIAL) == 1) and (hours.count(PREFERENTIAL) == 1):
    return 3, days.index(PREFERENTIAL), hours.index(PREFERENTIAL)
  elif (days.count(PREFERENTIAL) == 1) and (hours.count(AVAILABLE) == 1):
    return 2, days.index(PREFERENTIAL), hours.index(AVAILABLE)
  elif (days.count(AVAILABLE) == 1) and (hours.count(PREFERENTIAL) == 1):
    return 2, days.index(AVAILABLE), hours.index(PREFERENTIAL)
  elif (days.count(AVAILABLE) == 1) and (hours.count(AVAILABLE) == 1):
    return 1, days.index(AVAILABLE), hours.index(AVAILABLE)
  else:
    return 0, UNAVAILABLE, UNAVAILABLE

def shuffle_elements(values):
  days = values[0 : CL_DAYS]
  shuffle(days)
  hours = values[CL_HOURS-1 : ]
  shuffle(hours)
  
  string = ''
  for i in range(len(days)):
    if i:
      string += ' '
    string += days[i]
  for i in range(len(hours)):
    string += ' '
    string += hours[i]
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



######################## MAIN MAIN MAIN ##########################
######################## MAIN MAIN MAIN ##########################

print "\n"
print "=================================="
print "genxx: scr |  0  |  1  |  2  |  3 "
print "----------------------------------"
will_have_next_gen = 1
curr_gen = 0
scores = []
while will_have_next_gen:

  curr_score = 0
  mutation = int(CLASSES*RATIO/100)

  prefs = open("prefs", "r")
  curr = open("genxx/gen" + str(curr_gen).zfill(2), "r")
  next = open("genxx/gen" + str(curr_gen+1).zfill(2), "w")

  # counter variables to debug.
  pp = []
  for i in range(4):
    pp.append(0)

  for i in range(CLASSES):

    # allocation[x*CL_DAYS+y] represents day x at hour y
    # x from 0 (mon) to 4 (fri); y from 0 (8h) to 5 (21h)
    # it starts with 0 (zero) and is increased up to ROOMS
    allocation = []
    for i in range(CL_DAYS*CL_HOURS):
      allocation.append(0)

    pref_line = prefs.readline()
    pref_values = pref_line.split()
    curr_line = curr.readline()
    curr_values = curr_line.split()
    result, day, hour = bitwise(pref_values, curr_values)
    # pp is a debug variable
    pp[result] += 1
    if bool(result) and (allocation[day*CL_DAYS+hour] < ROOMS):
      curr_score += result
      allocation[day*CL_DAYS+hour] += 1
      next.write(curr_line)
    else:
      if (mutation > 0):
        next_line = shuffle_elements(curr_values)
        next.write(next_line)
        mutation -= 1;
      else:
        next.write(curr_line)

  # stop criteria
  if (curr_gen >= MIN_GENS) and (curr_score == scores[-1]) and (curr_score == scores[-2]):
    will_have_next_gen = 0

  scores.append(curr_score)
  #print "gen" + str(curr_gen).zfill(2) + ": " + str(scores[curr_gen]).zfill(3) + " | " + str(pp[0]).zfill(2) + " | " + str(pp[1]).zfill(2) + " | " + str(pp[2]).zfill(2) + " | " + str(pp[3]).zfill(2)
  print "gen%02d: %3d | %3d | %3d | %3d | %3d" % (curr_gen, scores[curr_gen], pp[0], pp[1], pp[2], pp[3])

  curr_gen += 1
  curr_score = 0

  prefs.close()
  curr.close()
  next.close()

print "=================================="
print "\n"
