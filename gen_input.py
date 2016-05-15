#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint

#parameters
CLASSES = 80
CL_DAYS = 5 # mon, tue, wed, thu, fri
CL_HOURS = 6 # 8, 10, 14, 16, 19, 21
MATCH = 1
MISMATCH = 0

f = open("input", "w")
for i in range(CLASSES):

  days = ""
  match_day = randint(0, CL_DAYS - 1)
  for j in range(CL_DAYS):
    if j != 0:
      days += " "
    if j == match_day:
      days += str(MATCH)
    else:
      days += str(MISMATCH)
  days += " "

  hours = ""
  match_hour = randint(0, CL_HOURS - 1)
  for j in range(CL_HOURS):
    if j != 0:
      hours += " "
    if j == match_hour:
      hours += str(MATCH)
    else:
      hours += str(MISMATCH)
  hours += "\n"

  f.write(days + hours)

f.close()
