import mne
import os
import os.path as op
import numpy as np
from function import prev_feedback, read_events

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
FB = [50, 51, 52, 53]   

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']

#data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'

for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                try:
                    tials_of_interest = np.loadtxt('/net/server/data/Archive/prob_learn/ksayfulina/events_clean_after_mio/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, t, fb), dtype='int')
                    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
                    if tials_of_interest.shape == (3,):
                        tials_of_interest = tials_of_interest.reshape(1,3)
                
                        # Load raw event with miocorection
                    events_raw = read_events('/net/server/data/home/inside/Events_probability/Events_clean/{0}_run{1}_events_clean.txt'.format(subj, r))
                        
                        
                        
                        #raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

                        #raw = mne.io.Raw(raw_fname, preload=True)

                        #events_raw = mne.find_events(raw, stim_channel='STI101', output='onset', 
                        #                         consecutive='increasing', min_duration=0, shortest_event=1, mask=None, 
                        #                         uint_cast=False, mask_type='and', initial_event=False, verbose=None)
                                                
                    prev_fb = prev_feedback(events_raw, tials_of_interest, FB)    
                        
                    np.savetxt("/net/server/data/Archive/prob_learn/vtretyakova/prev_fb_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}_prev_fb.txt".format(subj, r, t, fb), prev_fb, fmt="%s")
                    
                except OSError:
                    print('This file not exist')    
   
