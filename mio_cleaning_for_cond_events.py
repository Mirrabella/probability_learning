import mne
import os
import os.path as op
import numpy as np

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
 
   

rounds = [1, 2, 3, 4, 5, 6]


trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

for subj in subjects:
    for r in rounds:
    
        for t in trial_type:
            for fb in feedback:
                file_not_exist = []
                try:
                
                    events_mio_corrected = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/MIO/MIO_ALL/{0}_run{1}_events_mio_all.txt'.format(subj, r), dtype='int')
                    #events_mio_corrected = events_mio_corrected.tolist()
                    events_by_cond = np.loadtxt('/net/server/data/Archive/prob_learn/ksayfulina/events_clean_resp_TT_CF_time_not_corrected/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, t, fb), dtype='int')
                    
                    
                    
                    #events_by_cond = events_by_cond.tolist()
                    

                    events_by_cond_mio_corr = []
                    for i in events_by_cond:
                        if i in events_mio_corrected:
                            events_by_cond_mio_corr.append(i)
                            
                    events_by_cond_mio_corr = np.array(events_by_cond_mio_corr)
                    
                    n = np.size(events_by_cond_mio_corr)
                    
                    if n != 0:

                        np.savetxt("/net/server/data/Archive/prob_learn/vtretyakova/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}.txt".format(subj, r, t, fb), events_by_cond_mio_corr, fmt="%s")
                    else:
                        print('Empty array')
                except OSError:
                    
                    print('This file not exist')
                    

                    
                    
                    
