#!/bin/sh
# Plotting the modulation and phi of Z

fla=$1
flb=${fla}1

awk '{if (NF >= 3)
{
  if ($1 != "0" || $2 != "0")
  {
    print $1, $2, $3
  }
}
else
{
  print "   "
}
}' avhist.spt.${fla} > avhist.spt.${fla}.xx

awk '{if (NF >= 3)
{
  if ($1 != "0" || $2 != "0")
  {
    print $1, $2, $3
  }
}
else
{
  print "   "
}
}' avhist.spt.${flb} > avhist.spt.${flb}.xx

head -3 avhist.spt.${flb} | tail -1 >  avhist.spt.fpv_zero.${flb}.E.xx
head -3 avhist.spt.${flb} | tail -1 >> avhist.spt.fpv_zero.${flb}.E.xx
awk '{print $1, $2, $3}' avhist.spt.fpv_zero.${flb}.E.xx | sed  '2 s/0/1.0/' > avhist.spt.fpv_zero.${flb}.EL.xx

head -7 avhist.spt.${flb} | tail -1 > avhist.spt.fpv_zero.${flb}.I.xx
head -7 avhist.spt.${flb} | tail -1 >> avhist.spt.fpv_zero.${flb}.I.xx
awk '{print $1, $2, $3}' avhist.spt.fpv_zero.${flb}.I.xx | sed  '2 s/0/1.0/' > avhist.spt.fpv_zero.${flb}.IL.xx

xmgrace -graph 0 -settype xydy avhist.spt.fpv_zero.${flb}.EL.xx \
                               avhist.spt.fpv_zero.${flb}.IL.xx avhist.spt.${fla}.xx \
        -hdevice EPS -p ../scripts/avh_fpv.gr -printfile avh.${fla}.eps

