import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from functions import make_freq_stc, make_stc_epochs_from_freq_epochs


L_freq = 16
H_freq = 31
f_step = 2

#time_bandwidth = 4 #(by default = 4)
# if delta (1 - 4 Hz) 
#n_cycles = np.array([1, 1, 1, 2]) # уточнить


period_start = -1.750
period_end = 2.750

baseline = (-0.35, -0.05)

freq_range = 'beta_16_30'

description = 'STC for beta power 16 - 30 Hz, epochs, made from /net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_epo'

# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

# 40 subjects with all choice types

subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6


#subjects = subjects[22:] # from P033


rounds = [1, 2, 3, 4, 5, 6]

#trial_type = ['risk'] # on this step we'll make stc only for risk positive and negative fb
trial_type = ['norisk']
#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}'.format(freq_range), exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_epo'.format(freq_range), exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]


with open("/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_epo/config.txt".format(freq_range), "w") as file:
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
                
                    # stc with motphing
                    '''
                    stc_fsaverage = make_freq_stc(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, bem, src)
                    stc_fsaverage.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage/{1}_run{2}_{3}_fb_cur_{4}_{0}_stc'.format(freq_range, subj, r, cond, fb))
                    '''
                    # stc without morphing
                    '''
                    stc = make_freq_stc(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, bem, src)
                    stc.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_norisk_without_morph/{1}_run{2}_{3}_fb_cur_{4}_{0}_stc'.format(freq_range, subj, r, cond, fb))
                    '''
                    
                    # stc epochs
                    
                    stc = make_stc_epochs_from_freq_epochs(subj, r, cond, fb, data_path, baseline, bem, src)
                    print('Количество эпох %s' % len(stc))
                    
                    os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}'.format(freq_range, subj, r, cond, fb))
                    
                    for s in range(len(stc)):
                        stc[s].save('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}/{5}'.format(freq_range, subj, r, cond, fb, s))
                    
                except (OSError):
                    print('This file not exist')

