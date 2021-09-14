# https://mne.tools/stable/generated/mne.time_frequency.tfr_multitaper.html

import os.path as op
import numpy as np
import mne
import copy
import os
from functions import combined_planar_h5

freq_range = '2_40_step_2_time_bandwidth_by_default_4_early_log'
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

# донор (donor creation see make_donor.py)
# донор с 102 каналами (традиционно планар 1)
donor = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/donor_planar1_evoked.h5'.format(freq_range), condition=None)[0]

os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/{0}_comb_planars'.format(freq_range), exist_ok = True)
#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_20_tb_2_comb_planars/comb_planars_average_between_fb', exist_ok = True)
#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_20_tb_2_comb_planars/comb_planars_fb_separ', exist_ok = True)



for t in trial_type:
    for subj in subjects:
        try:
            evoked = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/ave_into_subj/{1}_{2}_{0}_resp.h5'.format(freq_range, subj, t), condition=None)
            
            # используем скрипт для того, чтобы создать комбайны
            
            _, _, comb_planar = combined_planar_h5(evoked)
            donor.data = comb_planar
            donor.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/{0}_comb_planars/{1}_{2}_average_{0}_resp_comb_planar.h5'.format(freq_range, subj, t))
            
            
        except (OSError):
            print('This file not exist')
            
        try:            
            evoked_positive = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/ave_into_subj_fb_positive/{1}_{2}_{0}_resp_fb_cur_positive.h5'.format(freq_range, subj, t), condition=None)
            _, _, comb_planar_positive = combined_planar_h5(evoked_positive)
            donor.data = comb_planar_positive
            donor.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/{0}_comb_planars/{1}_{2}_fb_cur_positive_average_{0}_resp_comb_planar.h5'.format(freq_range, subj, t))            
            
        except (OSError):
            print('This file not exist')            
            
            
        try:            
            
            evoked_negative = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/ave_into_subj_fb_negative/{1}_{2}_{0}_resp_fb_cur_negative.h5'.format(freq_range, subj, t), condition=None)
            
            _, _, comb_planar_negative = combined_planar_h5(evoked_negative)
            donor.data = comb_planar_negative
            donor.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/{0}_comb_planars/{1}_{2}_fb_cur_negative_average_{0}_resp_comb_planar.h5'.format(freq_range, subj, t))
            

            
        except (OSError):
            print('This file not exist')
            

