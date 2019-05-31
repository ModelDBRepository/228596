#!/usr/bin/python
# This program generates data files for running parameter surveys.

import sys
import math
import collections
#import numpy as np

# This function inserts par_now in line_read.
def insert_par_value(par_var_x, line_read, par_now):
    par_list = line_read.split()
#   print('par_list=', par_list)

    line_new = ''
    for par_sub in par_list:
        if '=' in par_sub:
            par_sub_unit = par_sub.split('=')
#           print ('par_sub_unit=', par_sub_unit[0], par_sub_unit[1])
            if par_var_x == par_sub_unit[0]:
                par_sub_unit[1] = par_now
            line_new += par_sub_unit[0] + '=' + str(par_sub_unit[1]) + ' '
        else:
            line_new += par_sub + ' '

    line_new = line_new[0:len(line_new)-1] + '\n'

#   print ('line_new=', line_new)

    return line_new

# This function checks whether parname_var appears in line_read. If it does, the function
# inserts par_now in line_read.
def check_for_parvar_and_change(dict_replace, line_read, appear_parname_block):
    line_new = line_read

    if ':' in dict_replace['parname_var']:
        parname_var_split = dict_replace['parname_var'].split(':')
        if parname_var_split[0] in line_read:
#           print ('parname_var=', parname_var_split)
            if parname_var_split[1] in line_read:
                line_new = insert_par_value(parname_var_split[1], line_read, dict_replace['par_now'])
    else:
        if dict_replace['parname_var'] in line_read:
            appear_parname_block = 2
            line_new = insert_par_value(dict_replace['parname_var'], line_read, dict_replace['par_now'])

#    line_new = line_read

    return (line_new, appear_parname_block)

# This function substitute the parameter that is replaced for all scan values and the scan values,
# and write one input file.
def write_one_input_file(dict_replace, dict_file_name, dict_scan):

    if ':' in dict_file_name['parname_var']:
        file_name_par = dict_file_name['parname_var'].split(':')[0]
    else:
        file_name_par = dict_file_name['parname_var']


    print ('sf=', dict_replace['suffix_r'])
    if dict_replace['suffix_r'] == 'none':
        file_name_read = 'tc.n.' + dict_scan['file_in_orig_suffix']
    else:
        file_name_read = 'tc.n.' + dict_replace['suffix_r'] + '.' +  file_name_par + '.' + \
        str(dict_file_name['ipar'])

    file_name_write = 'tc.n.' + dict_replace['suffix_w'] + '.' +  \
    file_name_par + '.' + str(dict_file_name['ipar'])
    print('file_name_read=', file_name_read, 'file_name_write=', file_name_write)

    fqsb.write('{0:s}\n'.format('tc_qsub ' + dict_replace['suffix_w'] + '.' + \
    file_name_par + '.' + str(dict_file_name['ipar'])))
    finr = open(file_name_read, 'r')
    finw = open(file_name_write, 'w')

    finw.write('{0:s}\n'.format(scan_line))
    if dict_replace['suffix_r'] == 'none':
        finw.write('{0:s} {1:s} parmin={2:f} parmax={3:f} npar={4:d} nrepeat={5:d}\n'.format( \
        dict_scan['parname_block'], dict_scan['parname_var'], \
        dict_scan['parmin'], dict_scan['parmax'], dict_scan['npar'], \
        dict_scan['nrepeat']))

    appear_parname_block = 0

    for line_read in finr:
        if line_read[0:4] != 'scan':
            if appear_parname_block == 0 or appear_parname_block == 2:
                finw.write('{0:s}'.format(line_read))
            elif appear_parname_block == 1:
                (line_new, appear_parname_block) = \
                check_for_parvar_and_change(dict_replace, line_read, \
                appear_parname_block)
                finw.write('{0:s}'.format(line_new))
            else:
                print ('wrong appear_parname_block=', appear_parname_block)

            len_parname_block = len(dict_replace['parname_block'])
            if appear_parname_block == 0 and \
            line_read[0:len_parname_block] == dict_replace['parname_block'][0:len_parname_block]:
                appear_parname_block = 1

    finr.close()
    finw.close()

# This function writes a series for input files as a parameter, such as synaptic strength, is varied.
# Files are generated for two values of Cv.
def write_series_input_files(dict_Cv, dict_curve, dict_scan, label1, label2):
    for dict_curve['ipar'] in range(0, dict_curve['npar']+1):
        if dict_curve['npar'] == 0:
            dict_curve['par_now'] = dict_curve['parmin']
        else:
            dict_curve['par_now'] = dict_curve['parmin'] + dict_curve['ipar'] * \
            (dict_curve['parmax'] - dict_curve['parmin']) / dict_curve['npar']

        dict_curve['suffix_r'] = 'none'
        dict_curve['suffix_w'] = label1
        write_one_input_file(dict_curve, dict_curve, dict_scan)

        if label2 != 'none':
            dict_Cv['parname_block'] = 'T_CELL'
            dict_Cv['parname_var'] = 'Cvmin'
            dict_Cv['suffix_r'] = label1
            dict_Cv['suffix_w'] = label2
            dict_Cv['par_now'] = 0.6
            dict_Cv['ipar'] = dict_curve['ipar']

            write_one_input_file(dict_Cv, dict_curve, dict_scan)

# main

fqsb = open('run_qsub.com', 'w')
fqsb.write('{0:s}\n'.format('#!/bin/sh'))
fqsb.write('{0:s}\n'.format('# Running the simulations.'))
fqsb.write('{0:s}\n'.format('  '))

dict_scan = dict()
dict_curve = dict()
dict_Cv = dict()

scan_line = 'scan=e'

# Feedback
dict_scan['file_in_orig_suffix'] = 'a1'

#-------------------------
# Curves that depend on Av
#-------------------------

dict_scan['parname_block'] = 'T_CELL'
dict_scan['parname_var'] = 'Av'
dict_scan['parmin'] = 20.0001
dict_scan['parmax'] = 0.0001
dict_scan['npar']= 20
dict_scan['nrepeat'] = 10

# ET
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'ET:gAMPA'
dict_curve['parmin'] = 0.0
dict_curve['parmax'] = 1.2
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'a', 'none')

# IT
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'PT:gAMPA'
dict_curve['parmin'] = 0.0
dict_curve['parmax'] = 1.6
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'a', 'none')

# EE
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'EE:gAMPA'
dict_curve['parmin'] = 0.0
dict_curve['parmax'] = 1.6
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'a', 'none')

# IE
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'PE:gAMPA'
dict_curve['parmin'] = 4.8
dict_curve['parmax'] = 0.0
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'a', 'none')

# EI
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'EP:gGABAA'
dict_curve['parmin'] = 5.6
dict_curve['parmax'] = 0.0
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'a', 'none')

# II
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'PP:gGABAA'
dict_curve['parmin'] = 4.4
dict_curve['parmax'] = 0.0
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'a', 'none')

#-------------------------
# Curves that depend on Cv
#-------------------------

dict_scan['parname_block'] = 'T_CELL'
dict_scan['parname_var'] = 'Cvmin'
dict_scan['parmin'] = 0.0
dict_scan['parmax'] = 1.2
dict_scan['npar']= 24
dict_scan['nrepeat'] = 10

# ET
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'ET:gAMPA'
dict_curve['parmin'] = 0.0
dict_curve['parmax'] = 1.2
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'c', 'none')

# IT
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'PT:gAMPA'
dict_curve['parmin'] = 0.0
dict_curve['parmax'] = 1.6
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'c', 'none')

#EE
#dict_curve['parname_block'] = 'SYNAPSE'
#dict_curve['parname_var'] = 'EE:gAMPA'
#dict_curve['parmin'] = 0.0
#dict_curve['parmax'] = 1.6
#dict_curve['npar'] = 10
#dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'c', 'none')

# IE
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'PE:gAMPA'
dict_curve['parmin'] = 4.8
dict_curve['parmax'] = 0.0
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'c', 'none')

# EI
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'EP:gGABAA'
dict_curve['parmin'] = 5.6
dict_curve['parmax'] = 0.0
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'c', 'none')

# II
dict_curve['parname_block'] = 'SYNAPSE'
dict_curve['parname_var'] = 'PP:gGABAA'
dict_curve['parmin'] = 4.4
dict_curve['parmax'] = 0.0
dict_curve['npar'] = 10
dict_curve['ipar'] = 0

write_series_input_files(dict_Cv, dict_curve, dict_scan, 'c', 'none')



fqsb.close()
