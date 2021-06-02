# усредняем данные для кажого испытуемого. Получаем Evoked на каждом сенсоре, а уже после будем считать комбайны

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

###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
cond_list = ['_norisk_fb_cur_positive',
             '_prerisk_fb_cur_positive',
             '_risk_fb_cur_positive',
             '_postrisk_fb_cur_positive',
             '_norisk_fb_cur_negative',
             '_prerisk_fb_cur_negative',
             '_risk_fb_cur_negative',
             '_postrisk_fb_cur_negative'
             ]

out_path='/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/' #path to epochs
f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


subj_list = subjects.copy()
for i,subject in enumerate(subjects):
    subject_files = [file for file in f if subject in file] #make list with all subject files 
    for j in cond_list: #check if subject has all conditions
        if not any(j in s for s in subject_files):
            if subject in subj_list:
                subj_list.remove(subject)

subjects = subj_list

print(len(subjects))

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

# донор
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P001_norisk_evoked_beta_16_30_resp.fif")

#feedback = ['positive', 'negative']

for t in trial_type:
    
    for subj in subjects:
        evoked_internal_subjects = []
        for r in rounds:
            try:
                #print(len(evoked_internal_subjects))    
                epochs_positive = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/{0}_run{1}_{2}_fb_cur_positive_beta_16_30-epo.fif'.format(subj, r, t), preload = True)
                epochs_negative = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/{0}_run{1}_{2}_fb_cur_negative_beta_16_30-epo.fif'.format(subj, r, t), preload = True)

                #эпохи соединяются как np.array и без извлечения данных (get_data())
                epochs = np.vstack([epochs_positive, epochs_negative])
                
                ################ Шаг усреднения 1 - усреднение внутри блока #################
                
                evoked = epochs.mean(axis=0) # shape 306 x  n, n - кол - во временных отчетов 
                # получаем список evoked усредненных внутри блока (длинна списка от 0 до 6, по количеству блоков)
                evoked_internal_subjects.append(evoked)
            except (OSError):
                print('This file not exist')
            
            
            if len(evoked_internal_subjects) > 0:
                #берем первый evoked, добавляем еще одну ось для блока
                evoked_array_for_subj = evoked_internal_subjects[0].reshape(1, 306, 1350)
                # так же добавляем еще одну ось для каждого блока и соединяем их в единый массив
                for i in np.arange(1, len(evoked_internal_subjects)):
                    a = evoked_internal_subjects[i].reshape(1, 306, 1350)
                    evoked_array_for_subj = np.vstack([evoked_array_for_subj, a])
                    
                    
                ############## Шаг усреднения 2 - усредняем данные внутри испытуемого #########################
                evoked_for_subject = evoked_array_for_subj.mean(axis = 0)
                
                # делаем Evoked с помощью донора (поскольку Evoked берем из тех же данных, то время не меняем)
                temp.data = evoked_for_subject
                # сохраняем данные, усредненные внутри испытуемого. Шаг усредения 3, это усреднение между испытуемыми делается при рисовании топомапов
                temp.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_2_steps/{0}_{1}_evoked_beta_16_30_resp.fif'.format(subj, t))
                
            else:
                pass
            
           
                    
            
            

                    
                    
