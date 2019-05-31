#!/bin/sh
# Touch: one parameter set, V and s averaged over cycles.

fla=b8
flb=b81
flc=b82

cat > touch_one_par_av_sed.xx <<EOF
s/Tall=6000.0/Tall=60000.0/
s/nt=120000/nt=1200000/
s/tstat=5500.0/tstat=59500.0/
s/traster=50000.0/traster=60000.0/
s/Cvmin=0.0/Cvmin=0.6/
EOF

sed -f touch_one_par_av_sed.xx tc.n.a1 > tc.n.${fla}
/bin/rm touch_one_par_av_sed.xx

cat > touch_one_par_av_sed.xx <<EOF
s/EE: gAMPA=0.8/EE: gAMPA=0.0/
EOF

sed -f touch_one_par_av_sed.xx tc.n.${fla} > tc.n.${flb}
/bin/rm touch_one_par_av_sed.xx

cat > touch_one_par_av_sed.xx <<EOF
s/EE: gAMPA=0.8/EE: gAMPA=1.4/
EOF

sed -f touch_one_par_av_sed.xx tc.n.${fla} > tc.n.${flc}
/bin/rm touch_one_par_av_sed.xx


../simulation_program/tc.ex ${fla}
../simulation_program/tc.ex ${flb}
../simulation_program/tc.ex ${flc}

../scripts/hpl_touch.com ${fla}
../scripts/hpl_touch.com ${flb}
../scripts/hpl_touch.com ${flc}
