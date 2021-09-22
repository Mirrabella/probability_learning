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

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

for t in trial_type:
    #data_for_each_subjects = []
    for subj in subjects:
        evoked_internal_subjects = []
        for r in rounds:
            for fb_cur in feedback:
                try:
                    epochs = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo_comb_planar/{0}_run{1}_{2}_fb_cur_{3}_beta_16_30-epo_comb_planar.fif'.format(subj, r, t, fb_cur), preload = True)
                    evoked = epochs.average()
                    evoked_internal_subjects.append(evoked)
                except (OSError):
                    print('This file not exist')
                    
        if len(evoked_internal_subjects) > 0: 
            ave_whithin_subject = mne.grand_average(evoked_internal_subjects) # усредняем данные внутри каждого испытуемого, т.е. между текущими фидбеками и блоками
            ave_whithin_subject.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/{0}_{1}_evoked_beta_16_30_resp_comb_planar.fif'.format(subj, t))
            #data_for_each_subjects.append(ave_whithin_subject)
        else:
            pass
    
   # print('Длина списка для гранд авередж %s'%len(data_for_each_subjects))

    #grand_averange = mne.grand_average(data_for_each_subjects)

   # grand_averange.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo_grand_average/ave_beta_16_30_resp_{0}.fif'.format(t))
                    
                    
