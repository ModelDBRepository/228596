#!/usr/bin/python
# This program compares the firing rates of two network simulations

import sys
import math
import collections
import os
import numpy as np

#main

epsilon = 1.0e-10
fracIextI = 0.5
nonI = 150
nonPV = int(fracIextI * nonI + epsilon)
print 'nonPV=', nonPV

fla = str(sys.argv[1]);
flb = str(sys.argv[2]);

fdata = open('tc.fri.' + fla, 'r')
fdatb = open('tc.fri.' + flb, 'r')
str_cmp = 'compfr.' + fla + '.' + flb
fcmp = open(str_cmp, 'w')
ffr1 = open(str_cmp + '.1.xx', 'w')
ffr2 = open(str_cmp + '.2.xx', 'w')
ffr3 = open(str_cmp + '.3.xx', 'w')
flin = open('line.xx', 'w')

for linea in fdata:
    lineb = fdatb.readline()
    var_lista = linea.split() 
    var_listb = lineb.split() 

    if len(var_lista) == 7:
        if var_lista[2] != var_listb[2] or var_lista[3] != var_listb[3]:
            print 'ipop=', var_lista[2], var_listb[2], 'ion=', var_lista[3], 
            var_listb[3]
            sys.exit()

        fra = float(var_lista[1]);
        frb = float(var_listb[1]);
        diff_fr = frb - fra
        fcmp.write('{0:g} {1:g} {2:d} {3:g} {4:g}\n'.format(float(var_listb[4]), diff_fr, int(var_lista[2]), fra, frb))

        if var_lista[2] == '2' and int(var_lista[3]) == nonPV:
            fcmp.write('   \n')

        if var_lista[2] == '1':
            ffr1.write('{0:g} {1:g}\n'.format(fra, frb))
        elif var_lista[2] == '2' and int(var_lista[3]) <= nonPV:
            ffr2.write('{0:g} {1:g}\n'.format(fra, frb))
        elif var_lista[2] == '2' and int(var_lista[3]) > nonPV:
            ffr3.write('{0:g} {1:g}\n'.format(fra, frb))
        else:
            print('ipop=', var_lista[2], ' ion=', var_lista[3])
            sys.exit()

    else:
        fcmp.write('   \n')

flin.write('0.0 0.0\n')
flin.write('100.0 100.0\n')

fdata.close()
fdatb.close()
fcmp.close()
ffr1.close()
ffr2.close()
ffr3.close()
flin.close()

xm_str = 'xmgrace -graph 0 ' + str_cmp + \
'                 -graph 1 ' + str_cmp + '.1.xx line.xx' + \
'                 -graph 2 ' + str_cmp + '.2.xx line.xx' + \
'                 -graph 3 ' + str_cmp + '.3.xx line.xx' + \
' -hdevice EPS -p ../scripts/compfr.gr -printfile compfr.' + fla + '.' + flb + '.eps'

#print(xm_str)

os.system(xm_str)
#D os.system('rm ' + str_cmp + '.?.xx')
