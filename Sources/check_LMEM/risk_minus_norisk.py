import mne
import os
import os.path as op
import numpy as np
import pandas as pd

# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

time_intervals = [0, 1, 2, 3, 4, 5]
# донор
temp = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_fsaverage/norisk', 'fsaverage')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).

risk = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_fsaverage/risk', 'fsaverage').data 
norisk = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_fsaverage/norisk', 'fsaverage').data     

diff = risk - norisk

print("diff shape = {0}".format(diff.shape))
temp.data = diff
temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/diff/hp_vs_lp_fsaverage')

###################### for few time intervals #################
for time in time_intervals:
    risk = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_short_int_fsaverage/{0}_risk'.format(time), 'fsaverage').data 
    norisk = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_short_int_fsaverage/{0}_norisk'.format(time), 'fsaverage').data     

    diff = risk - norisk

    print("diff shape = {0}".format(diff.shape))
    temp.data = diff
    temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/diff_short_int/{0}_hp_vs_lp_fsaverage'.format(time))
    
    
    
####################### resample ##################################

print('Start of averaging of resample data')
# донор
temp = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/ave_in_fb_resample_fsaverage/P001_norisk_fb_cur_negative', 'fsaverage')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).

risk = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_resample_fsaverage/risk', 'fsaverage').data 
norisk = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_resample_fsaverage/norisk', 'fsaverage').data     

diff = risk - norisk

print("diff shape = {0}".format(diff.shape))
temp.data = diff
temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/diff_resample/hp_vs_lp_fsaverage')







