import mne
import os
import os.path as op
import numpy as np
from function import make_beta_signal


L_freq = 16
H_freq = 31
f_step = 2

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
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo', exist_ok = True)
for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    epochs_tfr = make_beta_signal(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline)
                    epochs_tfr.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/{0}_run{1}_{2}_fb_cur_{3}_beta_16_30-epo.fif'.format(subj, r, cond, fb), overwrite=True)
                except (OSError):
                    print('This file not exist')


