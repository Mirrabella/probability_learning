import mne
import os
import os.path as op
import numpy as np
from function import fixation_cross_events, read_events


subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]


#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['norisk']

feedback = ['positive', 'negative']

data_path_raw = '/net/server/data/home/inside/Events_probability/Events_clean'
raw_name = '{0}_run{1}_events_clean.txt'
data_path_events = '/net/server/data/Archive/prob_learn/ksayfulina/events_clean_after_mio'
name_events = '{0}_run{1}_norisk_fb_{2}.txt'

for subj in subjects:
    for r in rounds:
    
        for t in trial_type:
            for fb in feedback:
                file_not_exist = []
                try:
                    event_fixation_cross_norisk = fixation_cross_events(data_path_raw, raw_name, data_path_events, name_events, subj, r, fb)
                
                    np.savetxt("/net/server/data/Archive/prob_learn/vtretyakova/fix_cross_mio_corr/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt".format(subj, r, t, fb), event_fixation_cross_norisk, fmt="%s")

                except OSError:
                   print('This file not exist')
                    

                    
                    
