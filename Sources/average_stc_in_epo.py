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

rounds = [1, 2, 3, 4, 5, 6]

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['risk']

feedback = ['positive', 'negative']
freq_range = 'beta_16_30'

os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/beta_16_30_stc_epo_average_epo', exist_ok = True)

# донор
temp = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/beta_16_30_stc_epo/P001_run2_norisk_fb_cur_negative_beta_16_30/0')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).



for subj in subjects:

    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                
                    epochs_num = os.listdir('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}_fsaverage'.format(freq_range, subj, r, cond, fb))
                    epo_n = int(len(epochs_num)/2)
                    #print(subj)
                    #print(r)
                    #print(fb)
                    print (epo_n)

                    epochs_all_array = np.zeros(shape=(epo_n, sn, n))

                    for ep in range(epo_n):
                        stc = mne.read_source_estimate("/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}_fsaverage/{5}".format(freq_range, subj, r, cond, fb, ep))
                        epochs_all_array[ep, :, :] = stc.data
                        
                    print(epochs_all_array.shape)
                    
                    stc_epo_ave = mne.SourceEstimate(data = epochs_all_array.mean(axis = 0), vertices = temp.vertices,  tmin = temp.tmin, tstep = temp.tstep)
                    stc_epo_ave.subject = subj
                    stc_epo_ave.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_epo_average_epo/{1}_{2}_fb_cur_{3}'.format(freq_range, subj, cond, fb))
                    
                except (OSError):
                    print('This file not exist')
                    
                    
                    
