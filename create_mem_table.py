
import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from mne import set_log_level
from function import make_subjects_df

#set_log_level("ERROR")

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
freq_range = 'alpha_8_12_trf_early_log'  

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']

# interval of interest (1800 ms +/- 100 ms)
tmin = -0.9
tmax = 2.501
step = 0.2

scheme = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/SCHEMES2.csv')
scheme = scheme.loc[222:]

os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/dataframe_for_LMEM_{0}'.format(freq_range), exist_ok = True)

########################## файл, со входными параметрами ############################################

lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin), "tmax = {}".format(tmax), "step = {} усредение сигнала +/- 1,0 step от значения над topomap  ".format(step)]


with open("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/dataframe_for_LMEM_{0}/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')

#####################################################################################################

for s in range(102):
    df = pd.DataFrame()
	
    for subj in subjects:
        for r in rounds:
            for t in trial_type:
                for fb_cur in feedback:
                    try:
                        combined_planar = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_epo_comb_planar/{1}_run{2}_{3}_fb_cur_{4}_{0}-epo_comb_planar.fif'.format(freq_range, subj, r, t, fb_cur), preload = True)
                        
                        df_subj = make_subjects_df(combined_planar, s, subj, r, t, fb_cur, tmin, tmax, step, scheme)
                        df = df.append(df_subj)            
                    except (OSError, FileNotFoundError):
                        print('This file not exist')
    df.to_csv('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/dataframe_for_LMEM_{0}/df_LMEM_{1}.csv'.format(freq_range, s))
                    
	
	
		

