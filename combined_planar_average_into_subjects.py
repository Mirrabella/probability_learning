import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
import copy
import pandas as pd
from scipy import stats
from function import combine_planar_Evoked


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


trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
# donor
donor = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif')


for t in trial_type:
    for subj in subjects:
        try:
            evoked = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_2_steps/{0}_{1}_evoked_beta_16_30_resp.fif'.format(subj, t))
            _, _, comb_planar = combine_planar_Evoked(evoked)
            donor.data = comb_planar
            donor.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_2_steps_comb_planar/{0}_{1}_evoked_beta_16_30_resp_comb_planar.fif'.format(subj, t))
        except (OSError):
            print('This file not exist')
            

