import mne
import os
import os.path as op
import numpy as np
import pandas as pd


subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6
# problems with subject 16 , when avereging 
subjects.remove('P016')

#test
#subjects = ['P001']

time_intervals = [0, 1, 2, 3, 4, 5]

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['norisk', 'risk']

freq_range = 'beta_16_30'

#создаем папку, куда будут сохраняться полученные файлы
#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/{0}/{0}_fsaverage_ave_into_subj_2step_united_fb'.format(freq_range), exist_ok = True)


# донор
temp = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/ave_in_fb_fsaverage/P001_norisk_fb_cur_negative', 'fsaverage')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).
'''
print('Start of averaging data in long time intervals')
for t in trial_type:
    data = np.empty((0, sn, n))
    for subj in subjects:
        
        

        try:
                    
                    
            stc = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/uni_fb_fsaverage/{0}_{1}'.format(subj, t), 'fsaverage').data                        
            stc = stc.reshape(1, sn, n) # добавляем ось subj
            data = np.vstack([data, stc])  # собираем всех испытуемых в один массив        
        except (OSError):
            #stc = np.empty((0, sn, n))
            print('file for %s %s not exist'%(subj, t))
                    
        
             
          # собираем все блоки в один массив
    print('data for all subjects has shape {0}'.format(data.shape))
            
                
    if data.size != 0:
        temp.data = data.mean(axis = 0)    # усредняем между subjects
        temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_fsaverage/{0}'.format(t))
    else:
        print('Subject has no data in this condition')
        pass
        
        
###################### for few time intervals #################

print('Start of averaging data in short time intervals')
for time in time_intervals:
    for t in trial_type:
        data = np.empty((0, sn, n))
        for subj in subjects:
            
            

            try:
                        
                        
                stc = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/uni_fb_short_int_fsaverage/{0}_{1}_{2}'.format(time, subj, t), 'fsaverage').data                        
                stc = stc.reshape(1, sn, n) # добавляем ось subj
                data = np.vstack([data, stc])  # собираем всех испытуемых в один массив        
            except (OSError):
                #stc = np.empty((0, sn, n))
                print('file for %s %s not exist'%(subj, t))
                        
            
                 
              # собираем все блоки в один массив
        print('data for all subjects has shape {0}'.format(data.shape))
                
                    
        if data.size != 0:
            temp.data = data.mean(axis = 0)    # усредняем между subjects
            temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_short_int_fsaverage/{0}_{1}'.format(time, t))
        else:
            print('Subject has no data in this condition')
            pass
'''        
########################### resample #######################################

print('Start of averaging of resample data')
# донор
temp = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/ave_in_fb_resample_fsaverage/P001_norisk_fb_cur_negative', 'fsaverage')

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).


for t in trial_type:
    data = np.empty((0, sn, n))
    for subj in subjects:
        
        

        try:
                    
                    
            stc = mne.read_source_estimate('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/uni_fb_resample_fsaverage/{0}_{1}'.format(subj, t), 'fsaverage').data                        
            stc = stc.reshape(1, sn, n) # добавляем ось subj
            data = np.vstack([data, stc])  # собираем всех испытуемых в один массив        
        except (OSError):
            #stc = np.empty((0, sn, n))
            print('file for %s %s not exist'%(subj, t))
                    
        
             
          # собираем все блоки в один массив
    print('data for all subjects has shape {0}'.format(data.shape))
            
                
    if data.size != 0:
        temp.data = data.mean(axis = 0)    # усредняем между subjects
        temp.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Check_LMEM/pooled_subj_resample_fsaverage/{0}'.format(t))
    else:
        print('Subject has no data in this condition')
        pass
        



  
