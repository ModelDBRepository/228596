#!/bin/sh
# Touch: one parameter set.

fl=b1

cat > touch_one_par.xx <<EOF
s/deltat=0.05 nt=120000/deltat=0.005 nt=600000/
s/twrite=10/twrite=1/
s/Cvmin=0.0/Cvmin=0.6/
EOF

sed -f touch_one_par.xx tc.n.a1 > tc.n.${fl}
/bin/rm touch_one_par.xx

../simulation_program/tc.ex ${fl}

../scripts/veit.com touch ${fl}
