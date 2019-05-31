#!/bin/sh
# Touch: one parameter set.

fla=b4

cat > touch_tau_delay_fsed.xx <<EOF
s/scan=n/scan=e\nSYNAPSE EP:tau_delay parmin=0.0 parmax=1.0 npar=10 nrepeat=10/
s/Cvmin=0.0/Cvmin=0.6/
EOF

sed -f touch_tau_delay_fsed.xx tc.n.a1 > tc.n.${fla}
/bin/rm touch_tau_delay_fsed.xx

../simulation_program/tc.ex ${fla}

../scripts/avhist.py ${fla}

../scripts/avh.com taud ${fla}


