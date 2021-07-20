import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul

###############################################################################################
######## function prepear .h5 files for tfr ploting ###########

def make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, freqs):
        
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
        
    
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		    
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)


    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
    
    '''    
        #add up all values according to the frequency axis
    b_line = freq_show_baseline.data.sum(axis=-2)
    '''
	# Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(freq_show_baseline.data, 0, 1)
    b_line = np.swapaxes(b_line, 1, 2)
	
	# выстраиваем в ряд бейзлайны для каждого из эвентов, как будто они происходили один за другим
    a, b, c, d = b_line.shape
    b_line = b_line.reshape(a, b, c * d)
	

    '''
	    # Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
    
    
        
        # выстраиваем в ряд бейзлайныbeta_16_30_epo_comb_planar для каждого из эвентов, как будто они происходили один за другим
    a, b, c = b_line.shape
    b_line = b_line.reshape(a, b * c)
    '''	    

	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		       
    epochs.resample(300) 

    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, use_fft = False, return_itc = False, average=False)

    '''
    temp = freq_show.data.sum(axis=2)
	'''
	
	####### Для данных так же меняем оси местами
    data = np.swapaxes(freq_show.data, 0, 1)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 2, 3)
	
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1)

    '''    
    ####### Для данных так же меняем оси местами
    data = np.swapaxes(temp, 0, 1)
    data = np.swapaxes(data, 1, 2)
	    
    # Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
	    
    b = b_line.mean(axis=-1)
    '''
    b_line_new_shape = b[:, :, np.newaxis, np.newaxis]
	
    '''    
    b_line_new_shape = b[:, np.newaxis, np.newaxis]
    '''
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 2, 3)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    
    freq_show.data = data
    
    return (freq_show)
    
    '''        
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
        
    freq_show.data = data
        
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
        
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
        
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
        
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = period_start, events = events_response)
        
    return (epochs_tfr)   
    '''



