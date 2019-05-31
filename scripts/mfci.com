#!/bin/sh
# Plotting the modulation and phi of Z

fl=$1
factor=$2 
python ../scripts/mps.py $fl $factor
python ../scripts/mps.py ${fl}1 $factor

awk '{if ($1 == "0") print $1, $2, $3}' mps.sfr.${fl}1 > mps.sfr.fpv_zero.${fl}1.xx

head -2 mps.sfr.fpv_zero.${fl}1.xx | tail -1 > mps.sfr.fpv_zero.${fl}1.E.xx
head -2 mps.sfr.fpv_zero.${fl}1.xx | tail -1 >> mps.sfr.fpv_zero.${fl}1.E.xx
sed  '2 s/0/1.0/' mps.sfr.fpv_zero.${fl}1.E.xx > mps.sfr.fpv_zero.${fl}1.EL.xx

head -3 mps.sfr.fpv_zero.${fl}1.xx | tail -1 > mps.sfr.fpv_zero.${fl}1.I.xx
head -3 mps.sfr.fpv_zero.${fl}1.xx | tail -1 >> mps.sfr.fpv_zero.${fl}1.I.xx
sed  '2 s/0/1.0/' mps.sfr.fpv_zero.${fl}1.I.xx > mps.sfr.fpv_zero.${fl}1.IL.xx

xmgrace -graph 0 -settype xydy mps.sfr.fpv_zero.${fl}1.EL.xx \
                               mps.sfr.fpv_zero.${fl}1.IL.xx mps.sfr.${fl} \
        -graph 1 -settype xydy mps.sfr.fpv_zero.${fl}1.EL.xx \
                               mps.sfr.fpv_zero.${fl}1.IL.xx mps.sfr.${fl} \
        -hdevice EPS -p ../scripts/mfci.fpv.gr -printfile mfci.$fl.eps

#D /bin/rm mps.sfr.fpv_zero.${fl}.xx
#D /bin/rm mps.sfr.fpv_zero.${fl}.E.xx mps.sfr.fpv_zero.${fl}.EL.xx
#D /bin/rm mps.sfr.fpv_zero.${fl}.I.xx mps.sfr.fpv_zero.${fl}.IL.xx
