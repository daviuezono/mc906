#!/bin/sh

if [ $# -ne 4 ]
  then
    echo '---> Usage: ./run.sh $CLASSES $MIN_GENS $ROOMS $RATIO'
    exit 1
fi

#parameters
CLASSES=$1
MIN_GENS=$2
ROOMS=$3
RATIO=$4

#script
python gen_input.py $CLASSES
python gen_prefs.py $CLASSES
mkdir genxx
cp input genxx/gen00
python main.py $CLASSES $MIN_GENS $ROOMS $RATIO
