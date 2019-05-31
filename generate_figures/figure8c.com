#!/bin/sh
# Touch: one parameter set.

fla=b9

cat > touch_gEE_fsed.xx <<EOF
s/scan=n/scan=e\nSYNAPSE EE:gAMPA parmin=0.0 parmax=1.6 npar=16 nrepeat=10/
s/Cvmin=0.0/Cvmin=0.6/
EOF

sed -f touch_gEE_fsed.xx tc.n.a1 > tc.n.${fla}
/bin/rm touch_gEE_fsed.xx

../simulation_program/tc.ex ${fla}

../scripts/avhist.py ${fla}

awk '{
if (NF >= 2)
{
  if ($1 < 1.61)
  {
    print $1 * 0.25, $2, $3, $4, $5
  }
}
else
{
print "  "
}
}' avhist.spt.${fla} > avhist.spt.${fla}.xx

/bin/mv avhist.spt.${fla}.xx avhist.spt.${fla}

../scripts/avh.com gEE ${fla}
