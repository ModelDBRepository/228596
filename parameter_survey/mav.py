#!/usr/bin/python
# This program computes statistics and standard deviation of FR, CV and chi 
# values from tc.avr.?? .

import sys
import math
import os
import numpy as np

# This function calculate the average and the standard deviation, given the
# sum, the sum of squares, and the number of data items.
def avr_sd_cal(sumvalZ, sumvalZsq, nparZ):
    if (nparZ <= 0):
        avvalZ = -999.9
        avvalZsq = -999.8
        diffZ = -999.7
        sigvalZ = -999.6
    else:
        avvalZ = sumvalZ / nparZ
        avvalZsq = sumvalZsq / nparZ
        diffZ = avvalZsq - avvalZ * avvalZ
        if (diffZ >= 0.0):
            sigvalZ = math.sqrt(diffZ)
        else:
            sigvalZ = -999.7

#    print 'nparZ=', nparZ, 'avvalZ=', avvalZ, 'sigvalZ=', sigvalZ

    return avvalZ, sigvalZ

# This function reads a specific column and writes the average and the
# standard deviation.
def one_column_calculate_statistics(flread, flwrite, col_num, factor):
    par_old = -999.999
    npar_all = 0
    nparZ = 0
    sumvalZ = 0.0
    sumvalZsq = 0.0
    
    flread.seek(0)

    for line in flread:
        val_list = line.split()
        par = float(val_list[0])
        valZ = float(val_list[col_num])
        npar_all += 1
    
        if par != par_old:
            if (npar_all > 1):
                avvalZ, sigvalZ = avr_sd_cal(sumvalZ, sumvalZsq, nparZ)
#               flwrite.write('{0:g} {1:g} {2:g} {3:d}\n'.format( \
#               par_old * factor, sumvalZ, sumvalZsq, nparZ)) 
                if (avvalZ >= 0.0):
                    flwrite.write('{0:g} {1:g} {2:g}\n'.format( \
                    par_old * factor, avvalZ, sigvalZ))
    
            nparZ = 1
            sumvalZ = valZ
            sumvalZsq = valZ * valZ
            par_old = par
        else:
            nparZ += 1
            sumvalZ += valZ
            sumvalZsq += valZ * valZ
    
    
    if (npar_all > 0):
        avvalZ, sigvalZ = avr_sd_cal(sumvalZ, sumvalZsq, nparZ)
        if (avvalZ >= 0.0):            
            flwrite.write('{0:g} {1:g} {2:g}\n'.format(par_old * factor, \
            avvalZ, sigvalZ))

# This function processes one line of parameter sets.
def process_one_curve_for_each_neuron_type(run_type, curve_par_type, fl_index, \
    factor, fsfrE, fsfrI):
    file_str = run_type + '.' + curve_par_type + '.' + str(fl_index)
    print 'file_str=', file_str

    favr = open('tc.avr.' + file_str, 'r')

    Nval_before = 8
    one_column_calculate_statistics(favr, fsfrE, Nval_before, factor)
    fsfrE.write('   \n')

    chi_cal = 1
    Nval_before = 13 + chi_cal
    one_column_calculate_statistics(favr, fsfrI, Nval_before, factor)
    fsfrI.write('   \n')

    favr.close()

# This function processes a set, defined by one parameter, of a line defined
# by another parameter.
def process_all_curve_for_a_two_parameter_set(run_type, curve_par_type, \
    fl_index_range, factor):

    file_str = run_type + '.' + curve_par_type
    fsfrE_name = 'mav.sfr.' + file_str + '.E'
    fsfrI_name = 'mav.sfr.' + file_str + '.I'

    fsfrE = open(fsfrE_name, 'w')
    fsfrI = open(fsfrI_name, 'w')

    for fl_index in fl_index_range:
        process_one_curve_for_each_neuron_type(run_type, curve_par_type, \
        fl_index, factor, fsfrE, fsfrI)

    fsfrE.close()
    fsfrI.close()

    xm_str = 'xmgrace -graph 0 ' + fsfrE_name + \
    '                 -graph 1 ' + fsfrI_name + \
    ' -hdevice EPS -p mav.' + file_str + '.gr ' + \
    ' -printfile mav.'      + file_str + '.eps'

    os.system(xm_str)

#---------------------

#main

factor = 1.0

run_type = 'a'

curve_par_type = 'ET'
fl_index_range = range(0, 11)
process_all_curve_for_a_two_parameter_set(run_type, curve_par_type, \
    fl_index_range, factor)

curve_par_type = 'PT'
fl_index_range = range(0, 11)
process_all_curve_for_a_two_parameter_set(run_type, curve_par_type, \
    fl_index_range, factor)

curve_par_type = 'EE'
fl_index_range = range(0, 11)
process_all_curve_for_a_two_parameter_set(run_type, curve_par_type, \
    fl_index_range, factor)

curve_par_type = 'PE'
fl_index_range = range(0, 11)
process_all_curve_for_a_two_parameter_set(run_type, curve_par_type, \
    fl_index_range, factor)

curve_par_type = 'EP'
fl_index_range = range(0, 11)
process_all_curve_for_a_two_parameter_set(run_type, curve_par_type, \
    fl_index_range, factor)

curve_par_type = 'PP'
fl_index_range = range(0, 11)
process_all_curve_for_a_two_parameter_set(run_type, curve_par_type, \
    fl_index_range, factor)


