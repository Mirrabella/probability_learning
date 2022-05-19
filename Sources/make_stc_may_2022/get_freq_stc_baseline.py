import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from functions import make_stc_epochs_for_baseline


L_freq = 16
H_freq = 31
f_step = 2

#period_start = -1.750
#period_end = 2.750

baseline = (-0.35, -0.05)

freq_range = 'beta_16_30'

description = 'получаем stc для бейзлайна, без логарифмирования и умножения на 10'

# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

# 40 subjects with all choice types

subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6


#subjects = subjects[22:] # from P033


rounds = [1, 2, 3, 4, 5, 6]

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']


#feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/not_trained_trials/{0}'.format(freq_range), exist_ok = True)
#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/not_trained_trials/{0}/{0}_stc_epo_var2'.format(freq_range), exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "baseline = {}".format(baseline)]


with open("/net/server/data/Archive/prob_learn/data_processing/beta_16_30_sources/stc_by_epo_baseline_sLoreta/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################


for subj in subjects:
    bem = mne.read_bem_solution('/net/server/data/Archive/prob_learn/data_processing/bem/{0}_bem.h5'.format(subj), verbose=None)
    src = mne.setup_source_space(subject =subj, spacing='ico5', add_dist=False ) # by default - spacing='oct6' (4098 sources per hemisphere)
    #src = mne.setup_source_space(subject =subj, spacing='oct5', add_dist=False ) # 1026 per hemishere
    #mne.write_source_spaces('/net/server/data/Archive/prob_learn/data_processing/src_1026_oct5/{0}_oct5_src.fif'.format(subj), src)
    trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/{0}-COR.fif'.format(subj)
    for r in rounds:
        #for cond in trial_type:
            #for fb in feedback:
            
                #read events
	            #events for baseline
	            # download marks of positive feedback
                try:
                    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
                    

                        # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
                    if events_pos.shape == (3,):
                        events_pos = events_pos.reshape(1,3)
                        
                except (OSError):
                    print('There is no positive fb in norisk %s, run %s'% (subj, r))
                    events_pos = np.empty((0,3), dtype="int")
                    
                # download marks of negative feedback      
                try:
                    events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
                
                
                    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
                    if events_neg.shape == (3,):
                        events_neg = events_neg.reshape(1,3) 
                        
                except (OSError):
                    print('There is no negative fb in norisk %s, %s'% (subj, r))
                    events_neg = np.empty((0,3), dtype="int")
                
                #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
                events = np.vstack([events_pos, events_neg])
                events = np.sort(events, axis = 0)
                
                if events.size == 0:
                    print('Jump to next condition, there is nothing to catch')

                else: 
                    try:
                                                        
                        # stc for epochs baseline
                                
                        stc_epo_bl_list = make_stc_epochs_for_baseline(subj, r, data_path, L_freq, H_freq, f_step, baseline, bem, src, events, trans)
                        print('%s, run %s' % (subj, r))
                        print('Количество эпох %s' % len(stc_epo_bl_list))
                                
                        os.makedirs('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_baseline_sLoreta/{1}_run{2}_baseline'.format(freq_range, subj, r))
                                
                        for s in range(len(stc_epo_bl_list)):
                            stc_epo_bl_list[s].save('/net/server/data/Archive/prob_learn/data_processing/{0}_sources/stc_by_epo_baseline_sLoreta/{1}_run{2}_baseline/{3}'.format(freq_range, subj, r, s))
                                
                                            
                     
                    except (OSError):
                        print('This file not exist')

                        


