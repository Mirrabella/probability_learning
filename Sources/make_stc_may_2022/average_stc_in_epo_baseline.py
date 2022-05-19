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
#subjects.remove('P016')
subjects = subjects[11:]

rounds = [1, 2, 3, 4, 5, 6]

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

#feedback = ['positive', 'negative']
freq_range = 'beta_16_30'

os.makedirs('/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/epo_baseline_log_and_averaged', exist_ok = True)

# донор
temp = mne.read_source_estimate('/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/stc_by_epo_baseline_sLoreta/P001_run2_baseline/0')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).

baseline_temp = temp.mean() #averaged by time points

for subj in subjects:

    for r in rounds:
        #for cond in trial_type:
            #for fb in feedback:
                try:
                
                    epochs_num = os.listdir('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_baseline_sLoreta/{1}_run{2}_baseline'.format(freq_range, subj, r))
                    epo_n = int(len(epochs_num)/2)
                    #print(subj)
                    #print(r)
                    #print(fb)
                    print (epo_n)

                    epochs_all_array = np.zeros(shape=(epo_n, sn, n))

                    for ep in range(epo_n):
                        stc = mne.read_source_estimate("/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_baseline_sLoreta/{1}_run{2}_baseline/{3}".format(freq_range, subj, r, ep))
                        data = 10*np.log10(stc.data) # make log transformation
                        
                        epochs_all_array[ep, :, :] = data
                        
                    print(epochs_all_array.shape)
                    
                    epochs_ave = epochs_all_array.mean(axis = 0) # averaged between epoches
                    baseline = epochs_ave.mean(axis = 1) # averaged by time points
                    baseline = baseline.reshape((sn, 1))
                    
                    print(f'baseline shape = {baseline.shape}')
                    
                    stc_baseline = mne.SourceEstimate(data = baseline, vertices = baseline_temp.vertices,  tmin = baseline_temp.tmin, tstep = baseline_temp.tstep)
                    stc_baseline.subject = subj
                    stc_baseline.save('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/epo_baseline_log_and_averaged/{1}_run{2}'.format(freq_range, subj, r))
                    
                except (OSError):
                    print('This file not exist')
                    
                    
                    
