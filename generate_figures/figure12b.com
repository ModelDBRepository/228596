#!/bin/sh
# Halo and no Touch: one parameter set.

flgeneric=a1
fla=c1
factor=1.0

cat > halo_no_touch_fsed.xx <<EOF
s/scan=n/scan=e\nP_CELL fracIext parmin=0.033334 parmax=0.966667 npar=10 nrepeat=10/
10,30 s/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=0.0 DelIext=0.0 fracIext=1.0/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=-2.0 DelIext=1.0 fracIext=0.5/
EOF

sed -f halo_no_touch_fsed.xx tc.n.${flgeneric} > tc.n.${fla}
/bin/rm halo_no_touch_fsed.xx

cat > halo_no_touch_fsed.xx <<EOF
s/P_CELL fracIext parmin=0.033334 parmax=0.966667 npar=10 nrepeat=10/P_CELL fracIext parmin=0.0 parmax=0.0 npar=0 nrepeat=10/
EOF

sed -f halo_no_touch_fsed.xx tc.n.${fla} > tc.n.${fla}1
	      
../simulation_program/tc.ex ${fla}
../simulation_program/tc.ex ${fla}1
	      
../scripts/mfci.com ${fla} $factor
