#!/bin/sh
# Plotting the membrane potentials of several E and I neurons.

touchtype=$1
fl=$2

# E
awk '{print $1, $4}' tc.col.${fl} > veit.vv.${fl}.E.1.xx
awk '{print $1, $8}' tc.col.${fl} > veit.vv.${fl}.E.2.xx
awk '{print $1, $12}' tc.col.${fl} > veit.vv.${fl}.E.3.xx
awk '{print $1, $16}' tc.col.${fl} > veit.vv.${fl}.E.4.xx
awk '{print $1, $20}' tc.col.${fl} > veit.vv.${fl}.E.5.xx
awk '{print $1, $24}' tc.col.${fl} > veit.vv.${fl}.E.6.xx
awk '{print $1, $28}' tc.col.${fl} > veit.vv.${fl}.E.7.xx
awk '{print $1, $32}' tc.col.${fl} > veit.vv.${fl}.E.8.xx

# I
awk '{print $1, $38}' tc.col.${fl} > veit.vv.${fl}.I.1.xx
awk '{print $1, $42}' tc.col.${fl} > veit.vv.${fl}.I.2.xx
awk '{print $1, $46}' tc.col.${fl} > veit.vv.${fl}.I.3.xx
awk '{print $1, $50}' tc.col.${fl} > veit.vv.${fl}.I.4.xx
awk '{print $1, $54}' tc.col.${fl} > veit.vv.${fl}.I.5.xx
awk '{print $1, $58}' tc.col.${fl} > veit.vv.${fl}.I.6.xx
awk '{print $1, $62}' tc.col.${fl} > veit.vv.${fl}.I.7.xx
awk '{print $1, $66}' tc.col.${fl} > veit.vv.${fl}.I.8.xx

python ../scripts/touch.py ${fl}

xmgrace -graph 0 veit.T.${fl} \
        -graph 1 veit.vv.${fl}.E.1.xx \
        -graph 2 veit.vv.${fl}.E.2.xx \
        -graph 3 veit.vv.${fl}.E.3.xx \
        -graph 4 veit.vv.${fl}.E.4.xx \
        -graph 5 veit.vv.${fl}.E.5.xx \
        -graph 6 veit.vv.${fl}.E.6.xx \
        -graph 7 veit.vv.${fl}.E.7.xx \
        -graph 8 veit.vv.${fl}.E.8.xx \
        -graph 9 veit.T.${fl} \
        -graph 10 veit.vv.${fl}.I.1.xx \
        -graph 11 veit.vv.${fl}.I.2.xx \
        -graph 12 veit.vv.${fl}.I.3.xx \
        -graph 13 veit.vv.${fl}.I.4.xx \
        -graph 14 veit.vv.${fl}.I.5.xx \
        -graph 15 veit.vv.${fl}.I.6.xx \
        -graph 16 veit.vv.${fl}.I.7.xx \
        -graph 17 veit.vv.${fl}.I.8.xx \
        -hdevice EPS -p ../scripts/veit_${touchtype}.gr -printfile veit.$fl.eps

