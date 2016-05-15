#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint
from sys import argv
from sys import exit

if len(argv) != 2:
  print "---> Usage: python gen_prefs.py $CLASSES"
  exit(0)

#parameters
CLASSES = int(argv[1])
CL_DAYS = 5 # mon, tue, wed, thu, fri
CL_HOURS = 6 # 8, 10, 14, 16, 19, 21
UNAVAILABLE = 0
AVAILABLE = 1
PREFERENTIAL = 2

f = open("prefs", "w")
for i in range(CLASSES):

  days = ""
  for j in range(CL_DAYS):
    if j != 0:
      days += " "
    days += str(randint(UNAVAILABLE, PREFERENTIAL))

  hours = ""
  for j in range(CL_HOURS):
    if j != 0:
      hours += " "
    hours += str(randint(UNAVAILABLE, PREFERENTIAL))

  f.write(days + " " + hours + "\n")

f.close()
