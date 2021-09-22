import mne
import os
import os.path as op
import numpy as np
import pandas as pd


subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
        
# следующие испытуемы удаляются из выборки по причине возраста (>40 лет), либо нерискующие
subjects.remove('P000')
subjects.remove('P020')
subjects.remove('P036')
subjects.remove('P049')
subjects.remove('P056')

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

freq_range = 'beta_16_30_trf_average'

#создаем папку, куда будут сохраняться полученные комбайны
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_ave_into_subj'.format(freq_range), exist_ok = True)


# донор
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P001_norisk_evoked_beta_16_30_resp.fif")

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.


for subj in subjects:
    for t in trial_type:
        
        for r in rounds:
            ############################### Positive feedback ################################
            try:
                evoked_pos = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_ave/{1}_run{2}_{3}_fb_cur_positive_{0}_ave.fif'.format(freq_range, subj, r, t)).data                        
                evoked_pos = evoked_pos.reshape(1, 306, 1350)
            
            except (OSError):
                evoked_pos = np.empty((0, n))
                print('This file not exist')
                
            ############################### Negative feedback ################################    
            try:
                evoked_neg = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_ave/{1}_run{2}_{3}_fb_cur_negative_{0}_ave.fif'.format(freq_range, subj, r, t)).data               
                evoked_neg = evoked_neg.reshape(1, 306, 1350)
                
            except (OSError):
                evoked_neg = np.empty((0, n))
                print('This file not exist')
            
            print( evoked_pos.size )
            print( evoked_neg.size )
            
            if evoked_neg.size == 0 and evoked_pos.size != 0:
                data_into_subj = evoked_pos
                
            elif evoked_neg.size != 0 and evoked_pos.size == 0:
                
                data_into_subj = evoked_neg
                
            elif evoked_neg.size != 0 and evoked_pos.size != 0:
                                        
                data_into_subj = np.vstack([evoked_neg, evoked_pos])
            
            else:
                data_into_subj = np.empty((0, n))
                                        
            print(data_into_subj.size)                            
                                        
            if data_into_subj.size != 0:                                        
                temp.data = data_into_subj.mean(axis = 0)
                temp.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))                       
            else:
                print('Subject has no feedbacks in this condition')
                pass
                
            #print(temp.data.shape)   

