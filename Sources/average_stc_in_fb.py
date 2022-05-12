import os.path as op
import os
import mne
import numpy as np
import pandas as pd


# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'


# 40 subjects with all choice types

subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6

# problems with subject 16 , when avereging with out morphing
subjects.remove('P016')

rounds = [1, 2, 3, 4, 5, 6]

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['risk', 'norisk']

feedback = ['positive', 'negative']
freq_range = 'beta_16_30'

#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/beta_16_30_stc_epo_average_epo_var2_no_morph', exist_ok = True)

# донор
temp = mne.read_source_estimate('/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/stc_by_epo_morphed_sLoreta/P001_run2_norisk_fb_cur_negative_fsaverage/0', 'fsaverage')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).

time = [-0.900, -0.300]

for subj in subjects:
    for cond in trial_type:
        
        for fb in feedback:
            average_in_fb = np.empty((0, sn))
            for r in rounds:
                try:
                    print('%s %s %s run%s'%(subj, cond, fb, r))
                    epochs_num = os.listdir('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_morphed_sLoreta/{1}_run{2}_{3}_fb_cur_{4}_fsaverage'.format(freq_range, subj, r, cond, fb))
                    epo_n = int(len(epochs_num)/2)
                    print(fb)
                    print (epo_n)
                    epochs_all_array = np.zeros(shape=(epo_n, sn))
                    for ep in range(epo_n):
                        stc = mne.read_source_estimate("/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_morphed_sLoreta/{1}_run{2}_{3}_fb_cur_{4}_fsaverage/{5}".format(freq_range, subj, r, cond, fb, ep))
                        
                        stc_on_interval = stc.copy().crop(tmin=time[0], tmax=time[1], include_tmax=True)

                        epochs_all_array[ep, :] = stc_on_interval.data.mean(axis = 1) # усредняем по времени
                    print("shape of epo data on %s - %s"%(r, epochs_all_array.shape))
                    average_in_fb = np.append(average_in_fb, epochs_all_array, axis=0)
                except (OSError):
                    print('This file not exist')    

                
            print("fb = %s, data for average %s"% (fb, average_in_fb.shape))            
            average = average_in_fb.mean(axis = 0) # усреднение внутри фибека (для каждого испытуемго получаем положительный и отрицательный фидбэк)
                
            average = average.reshape(sn, 1)
            #print(average.shape)
                
            temp.data = average
                
            temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/ave_in_fb_fsaverage/{0}_{1}_fb_cur_{2}'.format(subj, cond, fb))        
               
####################### for few intervals ######################    
time_intervals = [[-0.900, -0.800], [-0.800, -0.700], [-0.700, -0.600], [-0.600, -0.500], [-0.500, -0.400], [-0.400, -0.300]]
for ind, time in enumerate(time_intervals):
    for subj in subjects:
        for cond in trial_type:
            
            for fb in feedback:
                average_in_fb = np.empty((0, sn))
                for r in rounds:
                    try:
                        print('%s %s %s run%s'%(subj, cond, fb, r))
                        epochs_num = os.listdir('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_morphed_sLoreta/{1}_run{2}_{3}_fb_cur_{4}_fsaverage'.format(freq_range, subj, r, cond, fb))
                        epo_n = int(len(epochs_num)/2)
                        print(fb)
                        print (epo_n)
                        epochs_all_array = np.zeros(shape=(epo_n, sn))
                        for ep in range(epo_n):
                            stc = mne.read_source_estimate("/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_morphed_sLoreta/{1}_run{2}_{3}_fb_cur_{4}_fsaverage/{5}".format(freq_range, subj, r, cond, fb, ep))
                            
                            stc_on_interval = stc.copy().crop(tmin=time[0], tmax=time[1], include_tmax=True)

                            epochs_all_array[ep, :] = stc_on_interval.data.mean(axis = 1) # усредняем по времени
                        print("shape of epo data on %s - %s"%(r, epochs_all_array.shape))
                        average_in_fb = np.append(average_in_fb, epochs_all_array, axis=0)
                    except (OSError):
                        print('This file not exist')    

                    
                print("fb = %s, data for average %s"% (fb, average_in_fb.shape))            
                average = average_in_fb.mean(axis = 0) # усреднение внутри фибека (для каждого испытуемго получаем положительный и отрицательный фидбэк)
                    
                average = average.reshape(sn, 1)
                #print(average.shape)
                    
                temp.data = average
                    
                temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/ave_in_fb_short_int_fsaverage/{0}_{1}_{2}_fb_cur_{3}'.format(ind, subj, cond, fb))        


########################### resample #######################################
time = [-0.900, -0.200] # интервал до ответа
# Загружаем шаблон
temp = mne.read_source_estimate("/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/stc_by_epo_morphed_sLoreta/P001_run2_norisk_fb_cur_negative_fsaverage/0", 'fsaverage')
temp = temp.copy().crop(tmin=time[0], tmax=time[1], include_tmax=True)
temp = temp.resample(10)

tp = len(temp.times) #количество временных точек
sn = temp.data.shape[0] #количество источников

for subj in subjects:
    
    for cond in trial_type:
        print(subj)
        print(cond)
        average_in_fb = np.empty((0, sn, tp))
        for fb in feedback:
            for r in rounds:
                print(f'round {r}')
                try:
                    epochs_num = os.listdir('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_morphed_sLoreta/{1}_run{2}_{3}_fb_cur_{4}_fsaverage'.format(freq_range, subj, r, cond, fb))
                    epo_n = int(len(epochs_num)/2)
                    print(fb)
                    print (epo_n)
                    epochs_all_array = np.zeros(shape=(epo_n, sn, tp))
                    for ep in range(epo_n):
                        print(f'epochs {ep}')
                        stc = mne.read_source_estimate("/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_morphed_sLoreta/{1}_run{2}_{3}_fb_cur_{4}_fsaverage/{5}".format(freq_range, subj, r, cond, fb, ep), 'fsaverage')
                        stc_on_interval = stc.copy().crop(tmin=time[0], tmax=time[1], include_tmax=True)
                        stc_on_interval_reshape = stc_on_interval.resample(10) #10 point per second, one point +/- 50 ms
                        print('Resample data shape {0}'.format(stc_on_interval_reshape.data.shape))
                        
                        epochs_all_array[ep, :, :] = stc_on_interval.data
                        print('amount of epochs {0}'.format(epochs_all_array.shape))
                    average_in_fb = np.append(average_in_fb, epochs_all_array, axis=0)
                    print('amount in fb {0}'.format(average_in_fb.shape))
                except (OSError):
                    print('This file not exist')

            average = average_in_fb.mean(axis = 0) # усреднение внутри фибека (для каждого испытуемго получаем положительный и отрицательный фидбэк)
            
            temp.data = average
                
            temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/ave_in_fb_resample/{0}_{1}_fb_cur_{2}'.format(subj, cond, fb))        

                
