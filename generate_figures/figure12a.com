#!/bin/sh
# Halo and Touch: one parameter set.

flgeneric=a1
fl=d1

cat > halo_touch_fsed.xx <<EOF
s/scan=n/scan=e\nP_CELL fracIext parmin=0.033334 parmax=0.966667 npar=10 nrepeat=10/
s/Cvmin=0.0/Cvmin=0.6/
10,30 s/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=0.0 DelIext=0.0 fracIext=1.0/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=-2.0 DelIext=1.0 fracIext=0.5/
EOF

sed -f halo_touch_fsed.xx tc.n.${flgeneric} > tc.n.${fl}
/bin/rm halo_touch_fsed.xx

cat > halo_touch_fsed.xx <<EOF
s/P_CELL fracIext parmin=0.033334 parmax=0.966667 npar=10 nrepeat=10/P_CELL fracIext parmin=0.0 parmax=0.0 npar=0 nrepeat=10/
EOF

sed -f halo_touch_fsed.xx tc.n.${fl} > tc.n.${fl}1
/bin/rm halo_touch_fsed.xx

../simulation_program/tc.ex ${fl} &
../simulation_program/tc.ex ${fl}1 &

../scripts/avhist.py ${fl}
../scripts/avhist.py ${fl}1

../scripts/avh_fpv.com ${fl}
