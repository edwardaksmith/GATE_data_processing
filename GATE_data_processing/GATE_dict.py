import SimpleITK as sitk
import numpy as np
import scipy as sp
import skimage.io as io
import matplotlib.pyplot as plt
import os as os
import copy
import GATE_data_processing.GATE_readers as GATErdr


def dict_build(data='SLAB',*args):

    # Data Choice

    if data == 'SLAB':
        import GATE_data_processing.slab_fp as data_fp

    GATE_dict = {}

    # Base Simulation

    GATE_dict['base'] = GATErdr.sobp_output(data_fp.fp_orig)

    # LET Add Investigation

    if 'LET_add' in args:

        LETAdd = {}

        LETAdd['all_sim']['all_beams'] = GATErdr.sobp_output(data_fp.fp_LETAdd_ball)
        LETAdd['GATE_add']['b1'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b01)
        LETAdd['GATE_add']['b2'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b02)
        LETAdd['GATE_add']['b3'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b03)
        LETAdd['GATE_add']['b4'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b04)
        LETAdd['GATE_add']['b5'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b05)
        LETAdd['GATE_add']['b6'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b06)
        LETAdd['GATE_add']['b7'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b07)
        LETAdd['GATE_add']['b8'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b08)
        LETAdd['GATE_add']['b9'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b09)
        LETAdd['GATE_add']['b10'] = GATErdr.sobp_output(data_fp.fp_LETAdd_b10)

        LETAdd['GATE_add']['b_combined'] = GATErdr.sum_dict_keys(LETAdd['b1'], LETAdd['b2'], LETAdd['b3'],
                                                                 LETAdd['b4'], LETAdd['b5'], LETAdd['b6'],
                                                                 LETAdd['b7'], LETAdd['b8'], LETAdd['b9'],
                                                                 LETAdd['b10'])

        LETAdd['dose_weight']['dose_*_letd'] = \
            np.multiply(LETAdd['GATE_add']['b1']['letd'], LETAdd['GATE_add']['b1']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b2']['letd'], LETAdd['GATE_add']['b2']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b3']['letd'], LETAdd['GATE_add']['b3']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b4']['letd'], LETAdd['GATE_add']['b4']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b5']['letd'], LETAdd['GATE_add']['b5']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b6']['letd'], LETAdd['GATE_add']['b6']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b7']['letd'], LETAdd['GATE_add']['b7']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b8']['letd'], LETAdd['GATE_add']['b8']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b9']['letd'], LETAdd['GATE_add']['b9']['dose']) + \
            np.multiply(LETAdd['GATE_add']['b10']['letd'], LETAdd['GATE_add']['b10']['dose'])

        LETAdd['dose_weight']['dose'] = LETAdd['GATE_add']['b1']['dose'] + \
                                        LETAdd['GATE_add']['b2']['dose'] + \
                                        LETAdd['GATE_add']['b3']['dose'] + \
                                        LETAdd['GATE_add']['b4']['dose'] + \
                                        LETAdd['GATE_add']['b5']['dose'] + \
                                        LETAdd['GATE_add']['b6']['dose'] + \
                                        LETAdd['GATE_add']['b7']['dose'] + \
                                        LETAdd['GATE_add']['b8']['dose'] + \
                                        LETAdd['GATE_add']['b9']['dose'] + \
                                        LETAdd['GATE_add']['b10']['dose']

        LETAdd['dose_weight']['letd'] = np.divide(LETAdd['dose_weight']['dose_*_letd'],
                                                  LETAdd['dose_weight']['dose_*_letd'])

        GATE_dict['LET_add'] = LETAdd

    # MSS Investigation

    if 'LET_MSS' in args:

        MSS = {}

        MSS['N/A'] = GATErdr.sobp_output(data_fp.fp_SLInvest_1)
        MSS['0.01'] = GATErdr.sobp_output(data_fp.fp_SLInvest_2)
        MSS['0.02'] = GATErdr.sobp_output(GATE_dict['base'])
        MSS['0.04'] = GATErdr.sobp_output(data_fp.fp_SLInvest_3)
        MSS['0.06'] = GATErdr.sobp_output(data_fp.fp_SLInvest_4)
        MSS['0.08'] = GATErdr.sobp_output(data_fp.fp_SLInvest_5)
        MSS['0.1'] = GATErdr.sobp_output(data_fp.fp_SLInvest_6)
        MSS['0.15'] = GATErdr.sobp_output(data_fp.fp_SLInvest_7)
        MSS['0.2'] = GATErdr.sobp_output(data_fp.fp_SLInvest_8)
        MSS['0.5'] = GATErdr.sobp_output(data_fp.fp_SLInvest_9)

        GATE_dict['LET_MSS'] = MSS

    # LET Scoring Investigation

    if 'LET_score' in args:

        LET_score = {}

        LET_score['bone']['med'] = GATErdr.sobp_output(data_fp.fp_LET2Med_Bone, let_type='MATERIAL')

        LET_score['bone']['water'] = GATErdr.sobp_output(data_fp.fp_LET2Water_Bone)

        LET_score['water']['water'] = GATE_dict['base']

        LET_score['water']['med'] = GATErdr.sobp_output(data_fp.fp_LET2Med_Water, let_type='MATERIAL')

        GATE_dict['LET_score'] = LET_score

    return GATE_dict


