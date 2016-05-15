#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint

#parameters
CLASSES = 80
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
    days += str(randint(UNAVAILABLE, AVAILABLE))

  hours = ""
  for j in range(CL_HOURS):
    if j != 0:
      hours += " "
    hours += str(randint(UNAVAILABLE, AVAILABLE))

  f.write(days + " " + hours + "\n")

f.close()
