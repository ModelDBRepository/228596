#!/bin/sh
# Halo and no Touch: one parameter set, with and without halo, 
# changes in firing rates.

flgeneric=a1
fla=c3
factor=1.0

cat > halo_no_touch_at_fsed.xx <<EOF
s/scan=n/scan=e\nT_CELL Av parmin=0.0001 parmax=20.0001 npar=20 nrepeat=10/
10,30 s/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=0.0 DelIext=0.0 fracIext=1.0/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=-2.0 DelIext=1.0 fracIext=0.5/
EOF

sed -f halo_no_touch_at_fsed.xx tc.n.$flgeneric> tc.n.$fla
/bin/rm halo_no_touch_at_fsed.xx

../simulation_program/tc.ex $fla

../scripts/mfc.com ath $fla $factor
