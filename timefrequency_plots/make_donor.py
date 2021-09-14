


import os.path as op
import numpy as np
import mne
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch
import copy
import os
#from functions import make_h5_files


def make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs, meg = True):
        
    #read events
	#events for baseline
	# download marks of positive feedback
	
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
    
            # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_pos.shape == (3,):
        events_pos = events_pos.reshape(1,3)
        
    # download marks of negative feedback      
    
    events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_neg.shape == (3,):
        events_neg = events_neg.reshape(1,3) 
    
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    events = np.vstack([events_pos, events_neg])
    events = np.sort(events, axis = 0) 
    
    #events, which we need
    events_response = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}.txt'.format(subj, r, cond, fb), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_response.shape == (3,):
        events_response = events_response.reshape(1,3)
    
	           
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
        
    
    picks = mne.pick_types(raw_data.info, meg = meg, eog = True)
		    
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)

    # time_bandwidth = 4 , by default
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
    
    # логарифмируем данные для бейзлайн и получаем бейзлайн в дБ
    b_line = 10*np.log10(freq_show_baseline.data)
    '''
	# Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
    b_line = np.swapaxes(b_line, 1, 2)
	
	# выстраиваем в ряд бейзлайны для каждого из эвентов, как будто они происходили один за другим
    a, b, c, d = b_line.shape
    b_line = b_line.reshape(a, b, c * d)
    '''
	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		       
    epochs.resample(300) 
    # time_bandwidth = 4 , by default
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False)
    
    data = 10*np.log10(freq_show.data)
	
	####### Для данных так же меняем оси местами
    '''
    data = np.swapaxes(data, 0, 1)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 2, 3)
    '''
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1)
    b_line_new_shape = b[:, :, np.newaxis]

    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    
    data = data - b_line_new_shape
    #data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    '''
    data = np.swapaxes(data, 2, 3)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    '''
    freq_show.data = data
    
    return (freq_show)

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
L_freq = 2
H_freq = 41
f_step = 2

freqs = np.arange(L_freq, H_freq, f_step)

# if delta (1 - 4 Hz) 
#n_cycles = np.array([1, 1, 1, 2])

#for others
n_cycles = freqs//2

period_start = -1.750
period_end = 2.750

baseline = (-0.35, -0.05)

time_bandwidth = 4 #(4 by default)

freq_range = '2_40_step_2_time_bandwidth_by_default_4_early_log'

subjects = ['P001']
rounds = [2]
trial_type = ['risk']
feedback = ['negative']

for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    evoked_tfr_h5 = make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs)
                    evoked_tfr_h5.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/donor_evoked.h5'.format(freq_range, subj, r, cond, fb), overwrite=True)
                
                    evoked_tfr_h5_planar1 = make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs, meg = 'planar1')
                    evoked_tfr_h5_planar1.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/donor_planar1_evoked.h5'.format(freq_range, subj, r, cond, fb), overwrite=True)
                    evoked_tfr_h5_planar2 = make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs, meg = 'planar2')
                    evoked_tfr_h5_planar2.save('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/donor_planar2_evoked.h5'.format(freq_range, subj, r, cond, fb), overwrite=True)
                
                except (OSError):
                    print('This file not exist')

