#!/bin/sh
# No touch: one parameter set.

fl=f1

cat > no_touch_one_par.xx <<EOF
s/deltat=0.05 nt=120000/deltat=0.005 nt=600000/
s/twrite=10/twrite=1/
EOF

sed -f no_touch_one_par.xx tc.n.a1 > tc.n.${fl}
/bin/rm no_touch_one_par.xx

../simulation_program/tc.ex ${fl}

../scripts/veit.com notouch ${fl}
