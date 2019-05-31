#!/bin/sh
# Touch: one parameter set.

dir=$1
fla=b5

cat > touch_tAMPA_fsed.xx <<EOF
s/scan=n/scan=e\nSYNAPSE tAMPA parmin=1.0 parmax=4.5 npar=14 nrepeat=10/
s/Cvmin=0.0/Cvmin=0.6/
EOF

sed -f touch_tAMPA_fsed.xx tc.n.a1 > tc.n.${fla}
/bin/rm touch_tAMPA_fsed.xx

../simulation_program/tc.ex ${fla}

../scripts/avhist.py ${fla}

../scripts/avh.com tAMPA ${fla}
