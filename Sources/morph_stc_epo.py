
import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul

# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'


subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться
subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

#trial_type = ['norisk', 'prerisk', 'postrisk']

feedback = ['positive', 'negative']

rounds = [1, 2, 3, 4, 5, 6]

freq_range = 'beta_16_30'

#создаем папку, куда будут сохраняться полученные файлы
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_epo_var2'.format(freq_range), exist_ok = True)

# for stc epochs

for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    epochs_num = os.listdir('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}'.format(freq_range, subj, r, cond, fb))
                    #print(subj)
                    #print(r)
                    #print(fb)
                    print (int(len(epochs_num)/2))
                    os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}_fsaverage'.format(freq_range, subj, r, cond, fb))
                
                    for ep in range(int(len(epochs_num)/2)):
                    
                        stc= mne.read_source_estimate("/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}/{5}".format(freq_range, subj, r, cond, fb, ep))
                        morph = mne.compute_source_morph(stc, subject_from=subj, subject_to='fsaverage')
                        stc_fsaverage = morph.apply(stc)
                        stc_fsaverage.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}_fsaverage/{5}'.format(freq_range, subj, r, cond, fb, ep))
                        
                except (OSError):
                    print('This file not exist')



                    


