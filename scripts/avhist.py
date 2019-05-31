#!/usr/bin/python
# This program reads averages histograms of firing over repetitions

import sys
import math
import collections
import numpy as np


# this function reads the par line.
def read_p_line(var_dict, line):
    line_list = line.split()

    if line_list[0] != '#p':
        print 'found in line_p:', line_list[0]
        sys.exit(0)

    var_dict['ipar'] = int(line_list[1])
    var_dict['par'] = float(line_list[2])
    var_dict['nrepeat'] = int(line_list[3])

# this function reads the repeat line.
def read_r_line(var_dict, line):
    line_list = line.split()
#   print 'line_list_r=', line_list

    if line_list[0] != '#r':
        print 'found in line_r:', line_list[0]
        sys.exit(0)

    var_dict['irepeat'] = int(line_list[1])

# this function reads the histogram.
def read_hist_pop(var_dict, hist_one):
    len_line = 3

#   print 'npop=', var_dict['npop']
    ipop = 0

    while ipop < var_dict['npop']:
#        print 'ipop=', ipop 

        line = fhis.readline()
        line_list = line.split()
        line_len = len(line_list)
#        print 'line=', line, 'ipop=', ipop, ' line_list=', line_list, ' line_len=', line_len

        if line_len == 0:
            ipop += 1
        elif line_len == 3:
            ipop_read = int(line_list[2])
            ihist_read = int(line_list[0])

            if ihist_read > var_dict['nhist']:
                var_dict['nhist'] = ihist_read 

            hist_read = float(line_list[1])
#            print 'ipop=', ipop_read, 'ihist=', ihist_read, ' hist=', hist_read
            hist_one[ipop_read, ihist_read] = hist_read
        elif line_list[0][0:1] == '#':
            print 'line_list[0]=', line_list[0]
            sys.exit(0)

#       print ' ipop=', ipop, ' ipop_read=', ipop_read, 'ihist_read=', ihist_read, 'nhist=', var_dict['nhist']

# this function prints the histogram.
def print_hist(var_dict, hist_one, file_wrt):
    for ipop in range(0, var_dict['npop']):
        for ihist in range(0, var_dict['nhist']+1):
            file_wrt.write('{0:d} {1:g} {2:d}\n'.format(ihist, \
            hist_one[ipop, ihist], ipop)) 
        file_wrt.write('  \n')

# this function add hist_one to hist_all
def zero_hist_all(var_dict, hist_all, hist_all_t):
    for ipop in range(0, var_dict['npop']):

        for ihist in range(0, var_dict['mhist']):
            hist_all[ipop, ihist] = 0.0
            hist_all_t[ipop, ihist] = 0.0

# this function add hist_one to hist_all
def add_hist(var_dict, hist_one, hist_all, hist_all_t, tch_spk):
    for ipop in range(0, var_dict['npop']):

        for ihist in range(0, var_dict['nhist']+1):
            hist_all[ipop, ihist] += hist_one[ipop, ihist]
            hist_all_t[ipop, ihist] += hist_one[ipop, ihist] * \
            hist_one[ipop, ihist]

#       touch duration            
        touch_spk = 0.0
        for ihist in range(var_dict['imin'], var_dict['imax']):
            touch_spk += hist_one[ipop, ihist]
            fout.write('ipop={0:d} ihist={1:d} hist_one={2:g} touch_spk={3:g}\n'.format(ipop, ihist, hist_one[ipop, ihist], touch_spk))

#       print 'ipop=', ipop, ' touch_spk=', touch_spk

        touch_spk *= var_dict['tbin'] / 1000.0
 
        tch_spk['one_par_av'][ipop] += touch_spk
        tch_spk['one_par_avt'][ipop] += touch_spk * touch_spk
        
#       equal time before touch duration
        touch_spk = 0.0
        range_left = 2 * var_dict['imin'] - var_dict['imax'] - 1
        fout.write('imin={0:d} imax={1:d} range_left={2:d}\n'.format(var_dict['imin'], var_dict['imax'], range_left))
        for ihist in range(var_dict['imin']-1, range_left, -1):
            if ihist >= 0:
                jhist = ihist
            else:
                jhist = ihist + var_dict['nhist'] 
            touch_spk += hist_one[ipop, jhist]
            fout.write('ipop={0:d} jhist={1:d} hist_one={2:g} touch_spk={3:g}\n'.format(ipop, jhist, hist_one[ipop, jhist], touch_spk))

        touch_spk *= var_dict['tbin'] / 1000.0
        tch_spk['one_par_m_av'][ipop] += touch_spk
        tch_spk['one_par_m_avt'][ipop] += touch_spk * touch_spk
        

# this function add hist_one to hist_all
def div_hist_all(var_dict, hist_all, hist_all_t, tch_spk):
    for ipop in range(0, var_dict['npop']):

        for ihist in range(0, var_dict['nhist']+1):
            hist_all[ipop, ihist] /= var_dict['nrepeat']
            hist_all_t[ipop, ihist] /= var_dict['nrepeat']
 
        tch_spk['one_par_av'][ipop] /= var_dict['nrepeat']
        tch_spk['one_par_avt'][ipop] /= var_dict['nrepeat']
        tch_spk['one_par_m_av'][ipop] /= var_dict['nrepeat']
        tch_spk['one_par_m_avt'][ipop] /= var_dict['nrepeat']

# this function processes the realization-averaged histogram
def process_hist_all(var_dict, hist_all, hist_all_t, tch_spk):

    for ipop in range(0, var_dict['npop']):        
        print 'ipop=', ipop
        for ibin in range(var_dict['imin'], var_dict['imax']):
            diff_hist = hist_all_t[ipop, ibin] - \
            hist_all[ipop, ibin] * hist_all[ipop, ibin]

            if diff_hist > 0.0:
                sd_hist = math.sqrt(diff_hist)
            elif diff_hist > -var_dict['epsilon']:
                sd_hist = 0.0;
            else:
                print 'diff_hist=', diff_hist, '<0!', ' hist=', \
                hist_all[ipop, ibin], ' hist_t=', hist_all_t[ipop, ibin]
                sys.exit(0)

            fout.write('{0:d} {1:g} {2:g} {3:d}\n'.format(ibin, 
            hist_all[ipop, ibin], sd_hist, ipop))

        fout.write('  \n')

#       touch duration            
        diff_touch_spk = tch_spk['one_par_avt'][ipop] - \
        tch_spk['one_par_av'][ipop] * tch_spk['one_par_av'][ipop]

        if diff_touch_spk > 0.0:
            sd_touch_spk = math.sqrt(diff_touch_spk)
        elif diff_touch_spk >  -var_dict['epsilon']:
            sd_touch_spk = 0.0
        else:
            print 'diff_touch_spk=', diff_touch_spk, '<0!', ' touch_spk=', \
            tch_spk['one_par_av'][ipop], tch_spk['one_par_avt'][ipop]
            sys.exit(0)

        print '  ipop=', ipop, ' spk=', tch_spk['one_par_av'][ipop], \
        tch_spk['one_par_avt'][ipop], diff_touch_spk, sd_touch_spk
           
        tch_spk['one_par_sd'][ipop] = sd_touch_spk

#       equal time before touch duration
        diff_touch_spk = tch_spk['one_par_m_avt'][ipop] - \
        tch_spk['one_par_m_av'][ipop] * tch_spk['one_par_m_av'][ipop]

        if diff_touch_spk > 0.0:
            sd_touch_spk = math.sqrt(diff_touch_spk)
        elif diff_touch_spk >  -var_dict['epsilon']:
            sd_touch_spk = 0.0
        else:
            print 'diff_touch_spk=', diff_touch_spk, '<0!', ' touch_spk=', \
            tch_spk['one_par_av'][ipop], tch_spk['one_par_avt'][ipop]
            sys.exit(0)

        print 'm ipop=', ipop, ' spk=', tch_spk['one_par_m_av'][ipop], \
        tch_spk['one_par_m_avt'][ipop], diff_touch_spk, sd_touch_spk

        tch_spk['one_par_m_sd'][ipop] = sd_touch_spk

    tch_spk['all_par_av'].append(tch_spk['one_par_av'])
    tch_spk['all_par_sd'].append(tch_spk['one_par_sd'])
    tch_spk['all_par_m_av'].append(tch_spk['one_par_m_av'])
    tch_spk['all_par_m_sd'].append(tch_spk['one_par_m_sd'])

#   touch_spk_all_par_av.append([touch_spk_one_par_av[0], \
#   touch_spk_one_par_av[1], touch_spk_one_par_av[2]])
#   touch_spk_all_par_sd.append([touch_spk_one_par_sd[0], \
#   touch_spk_one_par_sd[1], touch_spk_one_par_sd[2]])


#main
suffix = str(sys.argv[1]);

fhis = open('tc.his.' + suffix, 'r')
favh =  open('avhist.his.' + suffix, 'w')
fspt = open('avhist.spt.' + suffix, 'w')
fout =  open('avhist.out.' + suffix, 'w')

var_dict = {}
var_dict['epsilon'] = 1.0e-10
var_dict['Tper'] = 100.0
#var_dict['Tmin'] = 20.0
#var_dict['Tmax'] = 30.0
var_dict['Tmin'] = 50.0
var_dict['Tmax'] = 75.0
var_dict['npop'] = 4
var_dict['nhist'] = 100
var_dict['mhist'] = 1001

var_dict['tbin'] = (var_dict['Tper'] + var_dict['epsilon']) /var_dict['nhist']
var_dict['imin'] = int((var_dict['Tmin'] + var_dict['epsilon']) / \
var_dict['tbin'])
var_dict['imax'] = int((var_dict['Tmax'] + var_dict['epsilon']) / \
var_dict['tbin'])
fout.write('nhist={0:d} imin={1:d} imax={2:d} Tmin={3:g} Tmax={4:g} ' \
           'tbin={5:g}\n'.format(var_dict['nhist'], var_dict['imin'], \
           var_dict['imax'], var_dict['Tmin'], var_dict['Tmax'], 
           var_dict['tbin']))

hist_all = np.zeros((var_dict['npop'], var_dict['mhist']), float)
hist_all_t = np.zeros((var_dict['npop'], var_dict['mhist']), float)
hist_one = np.zeros((var_dict['npop'], var_dict['mhist']), float)

par_list = []
tch_spk = {}
tch_spk['all_par_av'] = []
tch_spk['all_par_sd'] = []
tch_spk['all_par_m_av'] = []
tch_spk['all_par_m_sd'] = []

npar_read = -1

line = fhis.readline()
while line:
    tch_spk['one_par_av'] = []
    tch_spk['one_par_avt'] = []
    tch_spk['one_par_sd'] = []
    tch_spk['one_par_m_av'] = []
    tch_spk['one_par_m_avt'] = []
    tch_spk['one_par_m_sd'] = []
    for ipop in range(0, var_dict['npop']):
        tch_spk['one_par_av'].append(0.0)
        tch_spk['one_par_avt'].append(0.0)
        tch_spk['one_par_sd'].append(0.0)
        tch_spk['one_par_m_av'].append(0.0)
        tch_spk['one_par_m_avt'].append(0.0)
        tch_spk['one_par_m_sd'].append(0.0)

    zero_hist_all(var_dict, hist_all, hist_all_t)
    npar_read += 1
    read_p_line(var_dict, line)
    par_list.append(var_dict['par'])
#   print 'ipar=', var_dict['ipar'], ' par=', var_dict['par'], 'nrepeat=', \
#   var_dict['nrepeat']

    for jrepeat in range(1, var_dict['nrepeat']+1):
        line = fhis.readline()
        read_r_line(var_dict, line)
        read_hist_pop(var_dict, hist_one)
        print_hist(var_dict, hist_one, fout)
        add_hist(var_dict, hist_one, hist_all, hist_all_t, tch_spk)

    div_hist_all(var_dict, hist_all, hist_all_t, tch_spk)
    print_hist(var_dict, hist_all, favh)
    process_hist_all(var_dict, hist_all, hist_all_t, tch_spk)

    line = fhis.readline()

for ipop in range(0, var_dict['npop']):
    for ipar_read in range(0, npar_read+1):
        if tch_spk['all_par_sd'][ipar_read][ipop] > -var_dict['epsilon']:
            diff_all_par_av_m_av = tch_spk['all_par_av'][ipar_read][ipop] - \
            tch_spk['all_par_m_av'][ipar_read][ipop]
            sd__all_par_av_m_av = math.sqrt(
            math.pow(tch_spk['all_par_sd'][ipar_read][ipop], 2.0) +
            math.pow(tch_spk['all_par_m_sd'][ipar_read][ipop], 2.0))
            fspt.write('{0:g} '.format(par_list[ipar_read]))
            fspt.write('{0:g} '.format(diff_all_par_av_m_av))
            fspt.write('{0:g} '.format(sd__all_par_av_m_av))
            fspt.write(' {0:g} {1:g} a '.format(
            tch_spk['all_par_av'][ipar_read][ipop], 
            tch_spk['all_par_sd'][ipar_read][ipop]))
            fspt.write(' {0:g} {1:g} b '.format(
            tch_spk['all_par_m_av'][ipar_read][ipop], 
            tch_spk['all_par_m_sd'][ipar_read][ipop]))
            fspt.write(' {0:d} {1:d}\n'.format(ipar_read, ipop))

                                       
#       else:
#           fspt.write('{0:g} {1:g} {2:d} {3:d}\n'.format(
#           par_list[ipar_read], touch_spk_all_par_av[ipar_read][ipop], 
#           ipar_read, ipop))
        
    if ipop < var_dict['npop']:
        fspt.write('  \n')

fhis.close()
favh.close()
fspt.close()
fout.close()
