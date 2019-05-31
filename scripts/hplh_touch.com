#!/bin/sh
# Plotting the rastergram, with halo

fl=$1

python ../scripts/hth.py $1

xmgrace -graph 0 ht.hse.$1 \
        -graph 1 ht.hse.$1 \
        -graph 2 ht.hsi.$1 ht.hsh.$1 ht.hsnh.$1 \
        -graph 3 ht.hsi.$1 ht.hsh.$1 ht.hsnh.$1 \
        -graph 4 ht.hst.$1 \
        -graph 5 ht.hst.$1 \
        -hdevice EPS -p ../scripts/hplh_touch.gr -printfile hplh_touch.$fl.eps
