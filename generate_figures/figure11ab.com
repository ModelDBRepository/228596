#!/bin/sh
# Halo and no Touch: one parameter set, with and without halo, 
# changes in firing rates.

flgeneric=a1
fla=c2
flcomp=a3

cat > halo_fr_no_touch_fsed.xx <<EOF
10,30 s/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=0.0 DelIext=0.0 fracIext=1.0/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=-2.0 DelIext=1.0 fracIext=0.5/
s/Tall=6000.0/Tall=60000.0/
s/nt=120000/nt=1200000/
s/tstat=5500.0/tstat=59500.0/
s/traster=50000.0/traster=60000.0/
EOF

sed -f halo_fr_no_touch_fsed.xx tc.n.$flgeneric> tc.n.$fla
/bin/rm halo_fr_no_touch_fsed.xx

sed '16s/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=-2.0 DelIext=1.0 fracIext=0.5/gNa=100.0 gKdr=40.0 gKz=0.0 gL=0.1 DelgL=0.0 Iext=0.0 DelIext=0.0 fracIext=1.0/' tc.n.$fla > tc.n.$flcomp

../simulation_program/tc.ex $fla
../simulation_program/tc.ex $flcomp

../scripts/compfr.py $flcomp $fla
