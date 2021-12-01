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

# донор
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P001_norisk_evoked_beta_16_30_resp.fif")

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
freq_range = 'alpha_8_12_trf_early_log'

#создаем папку, куда будут сохраняться полученные комбайны
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_ave_into_subj'.format(freq_range), exist_ok = True)


for subj in subjects:
    for t in trial_type:
        ################################ Positive feedback ################################
        positive_fb = np.empty((0, 306, n))
        for r in rounds:
            try:
                               
                epochs_positive = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_positive_{0}_epo.fif'.format(freq_range, subj, r, t), preload = True)             

                
                positive_fb = np.vstack([positive_fb, epochs_positive.get_data()])
               
                
            except (OSError):
                
                print('This file not exist')

        ###### Шаг 1. Усреднили все положительные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if positive_fb.size != 0:
            positive_fb_mean = positive_fb.mean(axis = 0) 
            #positive_fb_mean = positive_fb_mean.reshape(1, 306, n) # добавляем ось для фидбека
            temp.data = positive_fb_mean
            temp.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_ave_into_subj/{1}_{2}_{0}_resp_fb_cur_positive.fif'.format(freq_range, subj, t))
            
        else:
            #positive_fb_mean = np.empty((0, 306, n))
            print('Subject has no positive feedbacks on this condition')
            
            
        ########################## Negative feedback #############################
        negative_fb = np.empty((0, 306, n))
        for r in rounds:
            try:
                               
                epochs_negative = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_negative_{0}_epo.fif'.format(freq_range, subj, r, t), preload = True)
                negative_fb = np.vstack([negative_fb, epochs_negative.get_data()])
             
                
            except (OSError):
                print('This file not exist')

        ###### Шаг 1. Усреднили все отрицательные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if negative_fb.size != 0:
            negative_fb_mean = negative_fb.mean(axis = 0) 
            #negative_fb_mean = negative_fb_mean.reshape(1, 306, n) # добавляем ось для фидбека
            
            
            temp.data = negative_fb_mean
            temp.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_ave_into_subj/{1}_{2}_{0}_resp_fb_cur_negative.fif'.format(freq_range, subj, t))
            

        else:
            print('Subject has no negative feedbacks on this condition')
            
            
