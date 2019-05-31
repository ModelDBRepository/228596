#!/bin/sh
# Touch: one parameter set.

fla=b2

cat > touch_at_fsed.xx <<EOF
s/scan=n/scan=e\nT_CELL Av parmin=0.0001 parmax=20.0001 npar=20 nrepeat=10/
s/Cvmin=0.0/Cvmin=0.6/
EOF

sed -f touch_at_fsed.xx tc.n.a1 > tc.n.${fla}
/bin/rm touch_at_fsed.xx

../simulation_program/tc.ex ${fla}

../scripts/avhist.py ${fla}

../scripts/avh.com at ${fla}
