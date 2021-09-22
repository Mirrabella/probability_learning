import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul








donor = mne.Evoked("/net/server/data/home/inside/beta_reactclean_15_26/030_koal_active2-end_react_beta-ave.fif") #donor

def make_beta_signal(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = 4):
    freqs = np.arange(L_freq, H_freq, f_step)
    
    #read events
	#events for baseline
	# download marks of positive feedback
	
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
    
    '''
    ####################################################
    #проверка скрипта Александры - нериск вместо фикс креста
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/ksayfulina/events_clean_after_mio/{0}_run{1}_norisk_fb_positive.txt".format(subj, r), dtype='int')
    #################################################
    '''
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
        
    
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		    
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)


    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
    
	#average between time points
    b_line  = freq_show_baseline.data.mean(axis=-1)
	

	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		       
    epochs.resample(300) 

    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False)
    
    temp = freq_show.data.sum(axis=1) #add up all values according to the frequency axis

    #add up all values according to the frequency axis for baseline
    b_line = b_line.sum(axis=1)
    b_line = b_line.reshape(temp.shape[0],1) #make shape 306 channels, one frequency (306 x 1)
    
    freq_show.data = temp.reshape(temp.shape[0],1,temp.shape[1]) #(306 x 1 x "time point amount")
    
    #b_line[:, :, np.newaxis].shape make baseline shape (306 X 1 X 1)
    
    freq_show.data = 10*np.log10(freq_show.data/b_line[:, :, np.newaxis]) #multyply by 10 for translation in dB
    
    
    
    
    '''	    
	####### Для данных так же меняем оси местами
    data = np.swapaxes(temp, 0, 1)
    data = np.swapaxes(data, 1, 2)
	    
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
	    
    b = b_line.mean(axis=-1)
	    
    b_line_new_shape = b[:, np.newaxis, np.newaxis]
            
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
        
    freq_show.data = data
        
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
    '''    
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
        
    new_evoked = donor.copy()
    new_evoked.info = freq_show.info
    new_evoked.nave = freq_show.nave
    new_evoked.kind = "average"
    new_evoked.times = freq_show.times
    new_evoked.first = 0
    new_evoked.last = new_evoked.times.shape[0] - 1
    new_evoked.comment = freq_show.comment

	#getting rid of the frequency axis	
    new_evoked.data = freq_show.data.mean(axis=1) 
        
    return (new_evoked)   
