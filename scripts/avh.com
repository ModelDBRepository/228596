#!/bin/sh
# Plotting R vs. a paraeter.

flgr=$1
fla=$2

awk '{if (NF >= 3)
{
  print $1, $2, $3
}
else
{
  print "   "
}
}' avhist.spt.${fla} > avhist.spt.${fla}.xx

xmgrace -graph 0 -settype xydy avhist.spt.${fla}.xx \
        -hdevice EPS -p ../scripts/avh.${flgr}.gr -printfile avh.${fla}.eps

#D /bin/rm avhist.spt.${fla}.xx
