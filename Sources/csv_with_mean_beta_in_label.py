
import mne
import numpy as np
import pandas as pd
import os


os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/subj_list.csv')['subj_list'].tolist()
subjects.remove('P062') 
subjects.remove('P052') 
subjects.remove("P032")
subjects.remove('P045') 

rounds = [1, 2, 3, 4, 5, 6]
freq_range = "beta_16_30"
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']
tmin = -0.800
tmax = 2.501
step = 0.1

scheme = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/SCHEMES2.csv')
scheme= scheme.loc[222:]

#parc that we used https://balsa.wustl.edu/WN56
labels =  mne.read_labels_from_annot("fsaverage", "HCPMMP1", hemi = "both")

data_path = "/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/stc_by_epo_morphed_sLoreta"

lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin), "tmax = {}".format(tmax), "step = {} усредение сигнала +/- 1,0 ms от значения".format(step)]


with open("/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/dataframe_for_LMEM/config.txt","w") as file:
    for  line in lines:
        file.write(line + '\n')
        
def make_subjects_df(label_stc, ep, subj, r, t, fb, tmin, tmax, step, scheme):
    '''
    time_intervals = np.arange(tmin, tmax, step)
    time_list = []
    for i in time_intervals:
        a = float(i)
        b = round(a, 1)
        time_list.append(b)
        
    list_of_time_intervals = []
    i = 0
    while i < (len(time_list) - 1):
        interval = time_list[i:i+2]
        list_of_time_intervals.append(interval)
            #print(interval)
        i = i+1
    '''
    list_of_time_intervals =[[-0.800, -0.700],[-0.700, -0.600],[-0.600,-0.500], [-0.500,-0.400], [-0.400,-0.300],
            [-0.300,-0.200],[-0.200,-0.100], [-0.100, 0.0], [0.0, 0.100],[0.100, 0.200],[0.200,0.300],
            [0.300,0.400],[0.400,0.500],[0.500, 0.600],[0.600,0.700],[0.700, 0.800],[0.800,0.900],[0.900, 1.000],
            [1.000, 1.100],[1.100,1.200],[1.200,1.300],[1.300,1.400],[1.400,1.500],[1.500,1.600],[1.600,1.700],
            [1.700,1.800],[1.800,1.900],[1.900,2.000], [2.000,2.100],[2.100,2.300],[2.300,2.400],[2.400,2.501]]
    
    mean_beta_on_intervals = []
    for time in list_of_time_intervals:
        label_in_interval = label_stc.copy().crop(tmin=time[0], tmax=time[1], include_tmax=True)
        
        mean_label_stc = np.mean(label_in_interval.data, axis=1) # averaging by time
        mean_label = np.mean(mean_label_stc.data, axis = 0) # average between vertexes
        mean_beta_on_intervals.append(mean_label) # list of mean beta power on each interval i current epoch
    
    
    feedback_prev_data = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/prev_fb_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}_prev_fb.txt".format(subj, r, t, fb), dtype='int')
    if feedback_prev_data.shape == (3,):
        feedback_prev_data = feedback_prev_data.reshape(1,3)
        

    FB_rew = [50, 51]
    FB_lose = [52, 53]
    
    if feedback_prev_data[ep][2] in FB_rew:
        feedback_prev = 'positive'
            
    else:
        feedback_prev = 'negative'

        
    # схема подкрепления   
    sch = scheme.loc[(scheme['fname'] == subj) & (scheme['block'] == r)]['scheme'].tolist()[0]

    # create DataFrame and save it in csv format
    df = pd.DataFrame()
    
    
    df['trial_number'] = [ep]
    
    # beta на интервалах
    for idx, beta in enumerate(mean_beta_on_intervals):
        df['beta power %s'%list_of_time_intervals[idx]] = [beta]
    

    #df['beta_power'] = beta_power
    df['subject'] = [subj]
    df['round'] = ['run{0}'.format(r)]
    df['trial_type'] = [t]
    df['feedback_cur'] = [fb]
    df['feedback_prev'] = [feedback_prev]
    df['scheme'] = [sch]
        
    return (df)



for label in labels:
    print(label)
    df = pd.DataFrame()
    for subj in subjects:
        for r in rounds:
            for t in trial_type:
                for fb in feedback:
                    
                    try:
                        epochs_num = os.listdir(os.path.join(data_path, '{0}_run{1}_{2}_fb_cur_{3}_fsaverage'.format(subj, r, t, fb)))
                        epo_n = (int(len(epochs_num) / 2))
                      
                        for ep in range(epo_n):
                            stc = mne.read_source_estimate(os.path.join(data_path, '{0}_run{1}_{2}_fb_cur_{3}_fsaverage/{4}'.format(subj, r, t, fb, ep)))
                            stc2 = stc.copy()
                            label_stc = stc2.in_label(label)
                            
                            df_subj = make_subjects_df(label_stc, ep, subj, r, t, fb, tmin, tmax, step, scheme)
                            df = df.append(df_subj)            
                    except (OSError, FileNotFoundError):
                        print('This file not exist')
    df.to_csv('/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/dataframe_for_LMEM/{0}.csv'.format(label))
                            
                            
