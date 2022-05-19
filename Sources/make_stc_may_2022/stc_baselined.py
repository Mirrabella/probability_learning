import os.path as op
import os
import mne
import numpy as np
import pandas as pd


# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'


# 40 subjects with all choice types

subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6

# problems with subject 16 , when avereging with out morphing
subjects.remove('P016')

rounds = [1, 2, 3, 4, 5, 6]

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['risk', 'norisk']

feedback = ['positive', 'negative']
freq_range = 'beta_16_30'

os.makedirs('/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/stc_sLoreta_baselined', exist_ok = True)

for subj in subjects:
    for r in rounds:
        try: 
            stc_baseline = mne.read_source_estimate('/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/epo_baseline_log_and_averaged/{0}_run{1}'.format(subj, r))
            
            
            
            for cond in trial_type:
                for fb in feedback:
                    try:
                        epochs_num = os.listdir('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_no_baseline_sLoreta/{1}_run{2}_{3}_fb_cur_{4}'.format(freq_range, subj, r, cond, fb))
                        epo_n = int(len(epochs_num)/2)
                        #print(subj)
                        #print(r), cond, fb
                        #print(fb)
                        print (f'{subj}, {cond} run {r},  {fb} number of epochs {epo_n}')
                        os.makedirs('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_sLoreta_baselined/{1}_run{2}_{3}_fb_cur_{4}'.format(freq_range, subj, r, cond, fb), exist_ok = True)
                        for ep in range(epo_n):
                            
                            stc = mne.read_source_estimate("/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_no_baseline_sLoreta/{1}_run{2}_{3}_fb_cur_{4}/{5}".format(freq_range, subj, r, cond, fb, ep))
                            data = 10*np.log10(stc.data) # make log transformation
                            
                            data_baselined = data - stc_baseline.data
                            
                            stc.data = data_baselined
                            
                            stc.save('/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/stc_sLoreta_baselined/{1}_run{2}_{3}_fb_cur_{4}/{5}'.format(freq_range, subj, r, cond, fb, ep))
                    
                    except (OSError):
                        print(f'{subj}, {cond} run {r},  {fb} has no data')
            
        except (OSError):
            print(f'{subj}, run {r} has no data for baseline')     
        


