#!/bin/sh
# Plotting the rastergram.

fl=$1

python ../scripts/ht.py $1

xmgrace -graph 0 ht.hse.$1 \
        -graph 1 ht.hse.$1 \
        -graph 2 ht.hsi.$1 \
        -graph 3 ht.hsi.$1 \
        -graph 4 ht.hst.$1 \
        -graph 5 ht.hst.$1 \
        -hdevice EPS -p ../scripts/hpl_touch.gr -printfile hpl_touch.$fl.eps
