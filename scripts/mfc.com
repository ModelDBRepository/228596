#!/bin/sh
# Plotting the modulation and phi of Z

runpar=$1
fl=$2
factor=$3

python ../scripts/mps.py $fl $factor

xmgrace -graph 0 -settype xydy mps.sfr.$fl \
        -graph 1 -settype xydy mps.sfr.$fl \
        -hdevice EPS -p ../scripts/mfc.$runpar.gr -printfile mfc.$fl.eps
