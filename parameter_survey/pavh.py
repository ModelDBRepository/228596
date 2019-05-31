#!/usr/bin/python
# This program reads averages histograms of firing over repetitions
# Baseline subtracted.

import sys
import math
import collections
import os
import numpy as np

# This function substitute values of parameters in var_dict, that remain
# the same for all curves.
def substitute_var_dict(var_dict):
    var_dict['epsilon'] = 1.0e-10
    var_dict['Tper'] = 100.0
#   var_dict['Tmin'] = 20.0
#   var_dict['Tmax'] = 30.0
    var_dict['Tmin'] = 50.0
    var_dict['Tmax'] = 75.0
    var_dict['npop'] = 4
    var_dict['nhist'] = 100
    var_dict['mhist'] = 1001
    
    var_dict['tbin'] = (var_dict['Tper'] + var_dict['epsilon']) / \
    var_dict['nhist']
    var_dict['imin'] = int((var_dict['Tmin'] + var_dict['epsilon']) / \
    var_dict['tbin'])
    var_dict['imax'] = int((var_dict['Tmax'] + var_dict['epsilon']) / \
    var_dict['tbin'])
    fout.write('nhist={0:d} imin={1:d} imax={2:d} Tmin={3:g} Tmax={4:g} ' \
               'tbin={4:g}\n'.format(var_dict['nhist'], var_dict['imin'], \
               var_dict['imax'], var_dict['Tmin'], var_dict['Tmax'], 
               var_dict['tbin']))

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
def read_hist_pop(var_dict, hist_one, fhis):
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


def process_one_curve_for_each_neuron_type(run_type, curve_par_type, fl_index, \
    factor, var_dict, run_type_index, fspt):
    file_str = run_type + '.' + curve_par_type + '.' + str(fl_index)
    print 'file_str=', file_str

    fhis = open('tc.his.'  + file_str, 'r')
#   favh =  open('pavh.his.' + file_str, 'r')

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
#       print 'ipar=', var_dict['ipar'], ' par=', var_dict['par'], 'nrepeat=', \
#       var_dict['nrepeat']

        for jrepeat in range(1, var_dict['nrepeat']+1):
            line = fhis.readline()
            read_r_line(var_dict, line)
            read_hist_pop(var_dict, hist_one, fhis)
#           print_hist(var_dict, hist_one, fout)
            add_hist(var_dict, hist_one, hist_all, hist_all_t, tch_spk)

        div_hist_all(var_dict, hist_all, hist_all_t, tch_spk)
#       print_hist(var_dict, hist_all, favh)
        process_hist_all(var_dict, hist_all, hist_all_t, tch_spk)

        line = fhis.readline()

    for ipop in range(0, var_dict['npop']):
        for ipar_read in range(0, npar_read+1):
            if tch_spk['all_par_sd'][ipar_read][ipop] > -var_dict['epsilon']:
                diff_all_par_av_m_av = tch_spk['all_par_av'][ipar_read][ipop]- \
                tch_spk['all_par_m_av'][ipar_read][ipop]
                sd__all_par_av_m_av = math.sqrt(
                math.pow(tch_spk['all_par_sd'][ipar_read][ipop], 2.0) +
                math.pow(tch_spk['all_par_m_sd'][ipar_read][ipop], 2.0))
                fspt[ipop].write('{0:g} '.format(par_list[ipar_read]))
                fspt[ipop].write('{0:g} '.format(diff_all_par_av_m_av))
                fspt[ipop].write('{0:g} '.format(sd__all_par_av_m_av))
                fspt[ipop].write(' {0:g} {1:g}  '.format(
                tch_spk['all_par_av'][ipar_read][ipop], 
                tch_spk['all_par_sd'][ipar_read][ipop]))
                fspt[ipop].write(' {0:g} {1:g}  '.format(
                tch_spk['all_par_m_av'][ipar_read][ipop], 
                tch_spk['all_par_m_sd'][ipar_read][ipop]))
                fspt[ipop].write(' {0:d} {1:d}\n'.format(ipar_read, ipop))
                        
        if ipop < var_dict['npop']:
            fspt[ipop].write('  \n')

    fhis.close()
#   favh.close()


# This function processes a set, defined by one parameter, of a line defined
# by another parameter.
def process_all_curve_for_a_two_parameter_set(run_type_list, curve_par_type, \
    fl_index_range, factor, var_dict):

    list_num_pop = ['T', 'E', 'I', 'S']
    list_file_name = []

    fspt_name_all_types = []
    for run_type_index in range(0, len(run_type_list)):
        run_type = run_type_list[run_type_index]
        print 'run_type=', run_type, ' run_type_list=', run_type_list
        file_str = run_type + '.' + curve_par_type

        list_file_name.append([])
        print 'run_type=', run_type, ' run_type_list=', run_type_list
        fspt = []
        fspt_name_all_types.append([])
        for ipop in range(0, var_dict['npop']):
            spt_str = 'pavh.spt.' + file_str + '.' + list_num_pop[ipop]
            list_file_name[run_type_index].append(spt_str)
            fspt_name_all_types[run_type_index].append(spt_str)
            fspt.append(open(fspt_name_all_types[run_type_index][ipop], 'w'))

        for fl_index in fl_index_range:
            print 'xspt_str=', spt_str
            process_one_curve_for_each_neuron_type(run_type, \
            curve_par_type, fl_index, factor, var_dict, run_type_index, fspt)

        for fla in fspt:
            fla.close()

    file_str = run_type_list[0] + '.' + curve_par_type

    xm_str = 'xmgrace -graph 0 ' 
    for run_type_index in range(0, len(run_type_list)):
        xm_str += fspt_name_all_types[run_type_index][1] + ' '
    xm_str += '-graph 1 ' 
    for run_type_index in range(0, len(run_type_list)):
        xm_str += fspt_name_all_types[run_type_index][2] + ' '
    xm_str += ' -hdevice EPS -p pavh.' + file_str + '.gr '
    xm_str += ' -printfile pavh.'      + file_str + '.eps'

    print xm_str
    os.system(xm_str)


# This function processes the data and plots the figures for simulations
# as functions of Av for various values of g_\alpha\beta
def process_curves_Av(run_type_list, factor, var_dict):

    set_feedback = ['a', 'b', 'c']
    set_feedforward = ['e', 'f', 'g']

    condition = 1
    if (run_type_list[0] in set_feedback or \
    run_type_list[0] in set_feedforward) and condition == 1:
        curve_par_type = 'ET'
        fl_index_range = range(0, 11)
        process_all_curve_for_a_two_parameter_set(run_type_list, \
        curve_par_type, fl_index_range, factor, var_dict)

    if (run_type_list[0] in set_feedback or \
    run_type_list[0] in set_feedforward) and condition == 1:
        curve_par_type = 'PT'
        fl_index_range = range(0, 11)
        process_all_curve_for_a_two_parameter_set(run_type_list, \
        curve_par_type, fl_index_range, factor, var_dict)

    condition = 1

#   if run_type_list[0] in set_feedback and condition == 1:
#       curve_par_type = 'EE'
#       fl_index_range = range(0, 11)
#       process_all_curve_for_a_two_parameter_set(run_type_list, \
#       curve_par_type, fl_index_range, factor, var_dict)

    condition = 1

    if run_type_list[0] in set_feedback and condition == 1:
        curve_par_type = 'PE'
        fl_index_range = range(0, 11)
        process_all_curve_for_a_two_parameter_set(run_type_list, \
        curve_par_type, fl_index_range, factor, var_dict)

    if (run_type_list[0] in set_feedback or \
    run_type_list[0] in set_feedforward) and condition == 1:
        curve_par_type = 'EP'
        fl_index_range = range(0, 11)
        process_all_curve_for_a_two_parameter_set(run_type_list, \
        curve_par_type, fl_index_range, factor, var_dict)

    if run_type_list[0] in set_feedback and condition == 1:
        curve_par_type = 'PP'
        fl_index_range = range(0, 11)
        process_all_curve_for_a_two_parameter_set(run_type_list, \
        curve_par_type, fl_index_range, factor, var_dict)

#main

fout =  open('pavh.out.all', 'w')

var_dict = {}
substitute_var_dict(var_dict)

factor = 1.0

run_type_list = ['c']
process_curves_Av(run_type_list, factor, var_dict)

fout.close()
