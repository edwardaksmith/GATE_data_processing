import SimpleITK as sitk
import numpy as np
import scipy as sp
import skimage.io as io
import matplotlib.pyplot as plt
import os as os
import copy

# General Functions

def clean_let_divide(let):

    ''' Input = LET np.array created from the dividing of let num and let den
        Output = LET np.array with Inf and NaN values removed'''

    let_clean = copy.deepcopy(let)

    # Setting nan values to zero and inf values to very high numbers
    let_clean = np.nan_to_num(let_clean)

    # Setting the inf related very high numbers to zero
    let_clean[let_clean > 1000] = 0

    return let_clean


def sum_dict_keys(f1, f2, f3, f4, f5, f6, f7, f8, f9, f10):

    ''' Input = three dicts with the same keys and same dimension np.array for each key
        Output = one dict with each key the sum of that key in the three original dicts'''

    f1_c = copy.deepcopy(f1)
    f2_c = copy.deepcopy(f2)
    f3_c = copy.deepcopy(f3)
    f4_c = copy.deepcopy(f4)
    f5_c = copy.deepcopy(f5)
    f6_c = copy.deepcopy(f6)
    f7_c = copy.deepcopy(f7)
    f8_c = copy.deepcopy(f8)
    f9_c = copy.deepcopy(f9)
    f10_c = copy.deepcopy(f10)

    f_all = {}

    for key, value in f1_c.items():

        all = f1_c[key] + f2_c[key] + f3_c[key] + f4_c[key] + f5_c[key] + f6_c[key] + f7_c[key] + f8_c[key] \
              + f9_c[key] + f10_c[key]

        f_all[key] = all

    f_all['lett'] = clean_let_divide(np.divide(f_all['lett_num'], f_all['lett_den']))

    f_all['letd'] = clean_let_divide(np.divide(f_all['letd_num'], f_all['letd_den']))

    return f_all



# Dictionary Creators

def F3_output(fp_output, let_type ='MATERIAL', particles = 'ALL PROTONS'):

    ''' This function converts the .mhd/.raw files from the 3 field GATE simulation into .npy and returns a dict.

    fp_gate_output = output folder containing the dose, lett, letd, flu of a simulation. etc
    '''

    gate_dict = {}

    # All Protons

    if os.path.isfile(fp_output + 'totaldose-Dose.mhd'):
        gate_dict['dose'] = io.imread(fp_output + 'totaldose-Dose.mhd', plugin='simpleitk')

    gate_dict['all_protons'] = {}

    if os.path.isfile(fp_output + 'fluence.mhd'):
        gate_dict['all_protons']['flu'] = io.imread(fp_output + 'fluence.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'lett-trackAveraged-numerator.mhd'):
        gate_dict['all_protons']['lett_num'] = io.imread(fp_output + 'lett-trackAveraged-numerator.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'lett-trackAveraged-denominator.mhd'):
        gate_dict['all_protons']['lett_den'] = io.imread(fp_output + 'lett-trackAveraged-denominator.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'letd-doseAveraged-numerator.mhd'):
        gate_dict['all_protons']['letd_num'] = io.imread(fp_output + 'letd-doseAveraged-numerator.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'letd-doseAveraged-denominator.mhd'):
        gate_dict['all_protons']['letd_den'] = io.imread(fp_output + 'letd-doseAveraged-denominator.mhd', plugin='simpleitk')

    # Primary protons only

    gate_dict['primary_protons'] = {}

    if os.path.isfile(fp_output + 'fluence_primary.mhd'):
        gate_dict['primary_protons']['flu'] = io.imread(fp_output + 'fluence_primary.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'lett_primary-trackAveraged-numerator.mhd'):
        gate_dict['primary_protons']['lett_num'] = io.imread(fp_output + 'lett_primary-trackAveraged-numerator.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'lett_primary-trackAveraged-denominator.mhd'):
        gate_dict['primary_protons']['lett_den'] = io.imread(fp_output + 'lett_primary-trackAveraged-denominator.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'letd_primary-doseAveraged-numerator.mhd'):
        gate_dict['primary_protons']['letd_num'] = io.imread(fp_output + 'letd_primary-doseAveraged-numerator.mhd', plugin='simpleitk')

    if os.path.isfile(fp_output + 'letd_primary-doseAveraged-denominator.mhd'):
        gate_dict['primary_protons']['letd_den'] = io.imread(fp_output + 'letd_primary-doseAveraged-denominator.mhd', plugin='simpleitk')

    return gate_dict


def sobp_output(filepath, let_type='WATER', actor_res='SLAB'):

    ''' This function converts the .mhd/.raw files from the 3 field GATE simulation into .npy and returns a dict.

    fp_gate_output = output folder containing the dose, lett, letd, flu of a simulation. etc

    '''

    simdict = {}

    # Custom tag build

    if let_type == 'WATER':
        let_type_s = 'letToWater-'
    elif let_type == 'MATERIAL':
        let_type_s = ''
    else:
        print('ERROR: INCORRECT let_type SET')

    # Dictionary creation

    simdict['dose'] = io.imread(filepath + 'total-Dose.mhd', plugin='simpleitk')

    simdict['letd_num'] = io.imread(filepath + 'letd-doseAveraged-' + let_type_s + 'numerator.mhd', plugin='simpleitk')
    simdict['letd_den'] = io.imread(filepath + 'letd-doseAveraged-' + let_type_s + 'denominator.mhd', plugin='simpleitk')
    simdict['lett_num'] = io.imread(filepath + 'lett-trackAveraged-' + let_type_s + 'numerator.mhd', plugin='simpleitk')
    simdict['lett_den'] = io.imread(filepath + 'lett-trackAveraged-' + let_type_s + 'denominator.mhd', plugin='simpleitk')

    simdict['letd'] = clean_let_divide(np.divide(simdict['letd_num'], simdict['letd_den']))
    simdict['lett'] = clean_let_divide(np.divide(simdict['lett_num'], simdict['lett_den']))

    if actor_res =='SLAB':
        for key, value in simdict.items():
            simdict[key] = np.ndarray.flatten(simdict[key])
    else:
        print('No flattening applied as actor_res=' + print(actor_res))
    return simdict
