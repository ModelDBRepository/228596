#!/usr/bin/python

import sys
import math
import collections

def write_hist_cal_Z(orderhist, Tper, nhist, fhs):
     zdict = dict()
     Z0 = 0.0
     Z1cos = 0
     Z1sin = 0

     for k, v in orderhist.iteritems(): 
          xx = k * Tper / nhist
          xxp = (k+1) * Tper / nhist
          xxh = (k+0.5) * Tper / nhist
#         fhs.write(str(xx) + ' ' + str(0) + '\n')
          fhs.write(str(xx) + ' ' + str( v) + '\n')
          fhs.write(str(xxp) + ' ' + str( v) + '\n')
#         fhs.write(str(xxp) + ' ' + str( 0) + '\n'
          Z0 += v
          Z1cos += v * math.cos(2.0 * math.pi * xxh / Tper)
          Z1sin += v * math.sin(2.0 * math.pi * xxh / Tper)

          if math.fabs(Z0) <= 1.0e-10:
               Z1md = 0.0
               Z1phi = -999.0
          else:
               Z1md = 2.0 *math.sqrt(Z1cos * Z1cos + Z1sin * Z1sin) / Z0
               Z1phi = math.atan2(Z1cos, Z1sin) / math.pi

#    print 'Z0=', Z0, 'Z1cos=', Z1cos, 'Z1sin=', Z1sin
#    print 'Z1md=', Z1md, 'Z1phi=', Z1phi
 
     zdict['Z1md'] = Z1md
     zdict['Z1phi'] = Z1phi

     fhs.write("   \n")
     return zdict


#--------


suffix = str(sys.argv[1]);
#print 'suffix=', suffix

fin  = open('tc.n.'   + suffix, 'r')
fspk = open('tc.ras.' + suffix, 'r')
fhst = open('ht.hst.' + suffix, 'w')
fhse = open('ht.hse.' + suffix, 'w')
fhsi = open('ht.hsi.' + suffix, 'w')
fout = open('ht.out.' + suffix, 'w')
histdicT = dict();
histdicE = dict();
histdicI = dict();

nfireT = dict();
for ion in range(200):
    nfireT[ion] = 0

line = fin.readline()
line = fin.readline()
line = fin.readline()
line = fin.readline()

line = fin.readline()
linespl = line.split(' ')

Av = float(linespl[0].split('=')[1])
Bv = float(linespl[1].split('=')[1])
Tper = float(linespl[2].split('=')[1])
phi_read = float(linespl[3].split('=')[1])
tcfrac = float(linespl[5].split('=')[1])
tauc = float(linespl[7].split('=')[1])

line = fin.readline()
linespl = line.split(' ')

Cvmin = float(linespl[1].split('=')[1])
Cvmax = float(linespl[2].split('=')[1])
#Cv = (Cvmin + Cvmax) / 2.0
Cv = Cvmin

line = fin.readline()
linespl = line.split(' ')

Tall = float(linespl[0].split('=')[1])
nonT = 200
nonE = 1600
nonI = 150

nhist = 500
deltat = Tper / nhist
ncut = 1000
Transient = 500.0

fout.write('Av={0:g} Bv={1:g} Cv={2:g} Tper={3:g} phi_read={4:g}\n'.format(Av, Bv, Cv, Tper, phi_read))

fout.write('tcfrac=%g tauc=%g\n' % (tcfrac, tauc))
fout.write('nhist=%d Tall=%g deltat=%g ncut=%d\n' % (nhist, Tall, deltat, ncut))
 
for tbin in range(nhist):
     histdicT[tbin] = 0.0
for tbin in range(nhist):
     histdicE[tbin] = 0.0
for tbin in range(nhist):
     histdicI[tbin] = 0.0

Tnspk = 0.0
TZcos = 0.0
TZsin = 0.0
Enspk = 0.0
EZcos = 0.0
EZsin = 0.0
Inspk = 0.0
IZcos = 0.0
IZsin = 0.0

for line in fspk:
    tspk = float((line.split())[0])

    if (tspk > Transient):
        ipop = int((line.split())[1])
        ion  = int((line.split())[2])
        tbin = int((tspk % Tper) / deltat)

        if ipop == 0:
            nfireT[ion-1] += 1

        if ipop == 0:
            if tbin not in histdicT:
                histdicT[tbin] = 1
            else:
                histdicT[tbin] += 1

            Tnspk += 1.0
            TZcos += math.cos(2.0 * math.pi * (tspk % Tper) / Tper)
            TZsin += math.sin(2.0 * math.pi * (tspk % Tper) / Tper)

        if ipop == 1:
            if tbin not in histdicE:
                histdicE[tbin] = 1
            else:
                histdicE[tbin] += 1

            Enspk += 1.0
            EZcos += math.cos(2.0 * math.pi * (tspk % Tper) / Tper)
            EZsin += math.sin(2.0 * math.pi * (tspk % Tper) / Tper)

        if ipop == 2:
            if tbin not in histdicI:
                histdicI[tbin] = 1
            else:
                histdicI[tbin] += 1

            Inspk += 1.0
            IZcos += math.cos(2.0 * math.pi * (tspk % Tper) / Tper)
            IZsin += math.sin(2.0 * math.pi * (tspk % Tper) / Tper)

spk_num_T = 0.0;
for ii in histdicT:
    histdicT[ii] *= (nhist / (Tall - Transient)) * 1000.0 / nonT

for ii in histdicE:
    histdicE[ii] *= (nhist / (Tall - Transient)) * 1000.0 / nonE

for ii in histdicI:
    histdicI[ii] *= (nhist / (Tall - Transient)) * 1000.0 / nonI

#    print ii, histdicT[ii]

fout.write('{0:s} {1:g}\n'.format('fspk_num_T=', spk_num_T))

#print histdicT

for ion in range(200):
    fout.write(str(ion+1) + ' ' + str(nfireT[ion]) + '\n')


orderhistT = collections.OrderedDict(sorted(histdicT.items()))
orderhistE = collections.OrderedDict(sorted(histdicE.items()))
orderhistI = collections.OrderedDict(sorted(histdicI.items()))
#print orderhist

zdict = write_hist_cal_Z(orderhistT, Tper, nhist, fhst)
print 'T: Zmd=', zdict['Z1md'], 'Zphi=', zdict['Z1phi']

zdict = write_hist_cal_Z(orderhistE, Tper, nhist, fhse)
print 'E: Zmd=', zdict['Z1md'], 'Zphi=', zdict['Z1phi']

zdict = write_hist_cal_Z(orderhistI, Tper, nhist, fhsi)
print 'I: Zmd=', zdict['Z1md'], 'Zphi=', zdict['Z1phi']

for ii in range(ncut):
    tt = (ii + 0.5 ) * Tper / ncut
    yy = Av * (1 + Bv * math.sin(2.0 * math.pi * tt / Tper + math.pi * phi_read)) 
    if tt > tcfrac * Tper and tt <  tcfrac * Tper + tauc:
        yy += + Cv * 1000.0 / tauc
    elif tt > (tcfrac - 1.0) * Tper and tt <  (tcfrac - 1.0) * Tper + tauc:
        yy += + Cv * 1000.0 / tauc

    fhst.write(str(tt) + ' ' + str(yy) + '\n')

TZmd = 2.0 *math.sqrt(TZcos * TZcos + TZsin * TZsin) / Tnspk
TZphi = math.atan2(TZcos, TZsin) / math.pi
print 'T: Zmd=', TZmd, 'Zphi=', TZphi, 'Zcos=', TZcos, 'Zsin=', TZsin, 'Tnspk=', Tnspk

EZmd = 2.0 *math.sqrt(EZcos * EZcos + EZsin * EZsin) / Enspk
EZphi = math.atan2(EZcos, EZsin) / math.pi
print 'E: Zmd=', EZmd, 'Zphi=', EZphi, 'Zcos=', EZcos, 'Zsin=', EZsin, 'Enspk=', Enspk

IZmd = 2.0 *math.sqrt(IZcos * IZcos + IZsin * IZsin) / Inspk
IZphi = math.atan2(IZcos, IZsin) / math.pi
print 'I: Zmd=', IZmd, 'Zphi=', IZphi, 'Zcos=', IZcos, 'Zsin=', IZsin, 'Inspk=', Inspk

        
fin.close()
fspk.close()
fhst.close()
fhse.close()
fhsi.close()
fout.close()
