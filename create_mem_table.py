
import mne
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
    
   

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']

# interval of interest (1800 ms +/- 100 ms)
tmin = -0.9
tmax = 2.501
step = 0.2

scheme = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/SCHEMES2.csv')
scheme = scheme.loc[222:]


for s in range(102):
    df = pd.DataFrame()
	
    for subj in subjects:
        for r in rounds:
            for t in trial_type:
                for fb_cur in feedback:
                    try:
                        combined_planar = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo_comb_planar/{0}_run{1}_{2}_fb_cur_{3}_beta_16_30-epo_comb_planar.fif'.format(subj, r, t, fb_cur), preload = True)
                        
                        df_subj = make_subjects_df(combined_planar, s, subj, r, t, fb_cur, tmin, tmax, step, scheme)
                        df = df.append(df_subj)            
                    except (OSError, FileNotFoundError):
                        print('This file not exist')
    df.to_csv('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/dataframe_for_LMEM/df_LMEM_{0}.csv'.format(s))
                    
	
	
		

