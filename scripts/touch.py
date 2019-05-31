#!/usr/bin/python

import sys
import math
import collections

suffix = str(sys.argv[1]);

ftch = open('veit.T.' + suffix, 'w')

epsilon = 1.0e-10
Tmax = 25000.0
Tper = 100.0
tcfrac = 0.5
tauc = 3.0

ncycle = int((Tmax + epsilon) / Tper)

tstim2 =  tcfrac * Tper + tauc


if tstim2 > Tper:
    tstim2 -= Tper
    ftch.write('0.0 60.0\n'.format())
    ftch.write('{0:g} 60.0\n'.format(tstim2))
    ftch.write('{0:g} 42.0\n'.format(tstim2))
else:
    ftch.write('0.0 30.0\n'.format())

for icycle in range (0, ncycle+1):
    tstim1 = (icycle + tcfrac) * Tper
    tstim2 = (icycle + tcfrac) * Tper + tauc
    ftch.write('{0:g} 42.0\n'.format(tstim1))
    ftch.write('{0:g} 60.0\n'.format(tstim1))
    ftch.write('{0:g} 60.0\n'.format(tstim2))
    ftch.write('{0:g} 42.0\n'.format(tstim2))


ftch.close()
