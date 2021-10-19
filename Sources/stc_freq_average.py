import mne
import os
import os.path as op
import numpy as np
import pandas as pd


subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться


#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['risk']

feedback = ['positive', 'negative']

freq_range = 'beta_16_30'

#создаем папку, куда будут сохраняться полученные файлы
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_average'.format(freq_range), exist_ok = True)


# донор
temp = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/beta_16_30_stc_fsaverage/P060_run5_risk_fb_cur_positive_beta_16_30_stc', 'fsaverage')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).


for t in trial_type:
    data_fb = np.empty((0, sn, n))
    for fb in feedback:
        for subj in subjects:
     
            try:
                stc = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_ave_into_subj/{1}_{2}_fb_cur_{3}'.format(freq_range, subj, t, fb), 'fsaverage').data                        
                stc = stc.reshape(1, sn, n) # добавляем ось испытуемого (subj)
                    
            except (OSError):
                stc = np.empty((0, sn, n))
                print('This file not exist')
                    
            data_fb = np.vstack([data_fb, stc])  # собираем всех испытуемых в один массив 
            #print(data_fb.shape)
                
        if data_fb.size != 0:
            temp.data = data_fb.mean(axis = 0)    # усредняем между испытуемыми (subj)
            temp.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_stc_fsaverage_average/{1}_fb_cur_{2}'.format(freq_range, t, fb))
        else:
            print('Subject has no feedbacks in this condition')
            pass
                    
