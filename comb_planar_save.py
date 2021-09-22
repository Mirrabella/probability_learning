import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from function import combine_planar_Epoches_TFR


# parametrs

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

tmin = -1.750

freq_range = 'alpha_8_12_trf_early_log'

os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_epo_comb_planar'.format(freq_range), exist_ok = True)
########################## файл, со входными параметрами ############################################

lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin)]


with open("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_epo_comb_planar/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')

#####################################################################################################



for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                try:
                    epochs = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}_epo.fif'.format(freq_range, subj, r, t, fb), preload = True)
                    combined_planar = combine_planar_Epoches_TFR(epochs, tmin)
                    combined_planar.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_epo_comb_planar/{1}_run{2}_{3}_fb_cur_{4}_{0}-epo_comb_planar.fif'.format(freq_range, subj, r, t, fb), overwrite=True)
                    
                    
                except (OSError, FileNotFoundError):
                    print('This file not exist')

