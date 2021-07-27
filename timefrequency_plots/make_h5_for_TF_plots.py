

import os.path as op
import numpy as np
import mne
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch
import copy
import os
from functions import make_h5_files


L_freq = 2
H_freq = 41
f_step = 2

freqs = np.arange(L_freq, H_freq, f_step)

# if delta (1 - 4 Hz) 
#n_cycles = np.array([1, 1, 1, 2])

#for others
n_cycles = freqs//2

period_start = -1.750
period_end = 2.750

baseline = (-0.35, -0.05)



subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots', exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_40_epo', exist_ok = True)

for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    epochs_tfr_h5 = make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, freqs)
                    epochs_tfr_h5.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_40_epo/{0}_run{1}_{2}_fb_cur_{3}_h5_2_40_epo-epo.h5'.format(subj, r, cond, fb), overwrite=True)
                except (OSError):
                    print('This file not exist')


