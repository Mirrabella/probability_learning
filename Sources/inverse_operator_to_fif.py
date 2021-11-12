import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from functions import make_inverse_operator

period_start = -1.750
period_end = 2.750
baseline = (-0.35, -0.05)

#freq_range = 'beta_16_30'

description = 'Inverse operators for each subject and each run'

# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

# 40 subjects with all choice types

subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
out_path = os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/inverse_operators', exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = [description, "baseline = {}".format(baseline)]


with open("/net/server/data/Archive/prob_learn/vtretyakova/sources/inverse_operators/config.txt", "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################


for subj in subjects:
    bem = mne.read_bem_solution('/net/server/data/Archive/prob_learn/vtretyakova/sources/bem/{0}_bem.h5'.format(subj), verbose=None)
    src = mne.setup_source_space(subject =subj, spacing='ico5', add_dist=False ) # by default - spacing='oct6' (4098 sources per hemisphere)
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    inv = make_inverse_operator(subj, r, cond, fb, data_path, baseline, period_start, period_end, bem, src)
                    fname = '/net/server/data/Archive/prob_learn/vtretyakova/sources/inverse_operators/{0}_run{1}_{2}_fb_cur_{3}-inv.fif'.format(subj, r, cond, fb)
                    mne.minimum_norm.write_inverse_operator(fname, inv, verbose=None)
                                        
                except (OSError):
                    print('This file not exist')

    

