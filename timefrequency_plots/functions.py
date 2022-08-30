

import os
from scipy import stats, io
import re
import mne
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul

###############################################################################################
######## function prepear .h5 files for tfr ploting ###########
# time_bandwidth = 4 by default
def make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs):
        
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

    # time_bandwidth = 4 , by default
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
    
    # логарифмируем данные для бейзлайн и получаем бейзлайн в дБ
    b_line = 10*np.log10(freq_show_baseline.data)
	# Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
    b_line = np.swapaxes(b_line, 1, 2)
	
	# выстраиваем в ряд бейзлайны для каждого из эвентов, как будто они происходили один за другим
    a, b, c, d = b_line.shape
    b_line = b_line.reshape(a, b, c * d)

	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		       
    epochs.resample(300) 
    # time_bandwidth = 4 , by default
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, average=False)
    
    data = 10*np.log10(freq_show.data)
	
	####### Для данных так же меняем оси местами
    data = np.swapaxes(data, 0, 1)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 2, 3)
	
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1)
    b_line_new_shape = b[:, :, np.newaxis, np.newaxis]

    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    
    data = data - b_line_new_shape
    #data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 2, 3)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    
    freq_show.data = data
    
    return (freq_show)

###############################################################################################
######## make combined planar .h5 files for tfr ploting ###########

def combined_planar_h5 (tfr):
    tfr1 = tfr[0]
    ep_TFR_planar1 = tfr1.copy(); 
    ep_TFR_planar2 = tfr1.copy()
    ep_TFR_planar1.pick_types(meg='planar1')
    ep_TFR_planar2.pick_types(meg='planar2')

    planar1 = ep_TFR_planar1.data
    planar2 = ep_TFR_planar2.data
    
    #grad_RMS = np.power((np.power(evk_planar1.data, 2) + np.power(evk_planar2.data, 2)), 1/2)
    combined = ep_TFR_planar1.data + ep_TFR_planar2.data
        
    return (planar1, planar2, combined)
    
###############################################################################################    
############################ FUNCTION FOR TTEST ############################
######################### парный ttest #########################################    
    
def ttest_pair_comb_channels(data_path, subjects, parameter1, parameter2, freq_range, planar,fr, n, best_chan_list): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 2, 102, fr, n))
    
    for ind, subj in enumerate(subjects):
        temp1 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_average_{2}_resp_{3}.h5'.format(subj, parameter1, freq_range, planar)))[0]
        temp2 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_average_{2}_resp_{3}.h5'.format(subj, parameter2, freq_range, planar)))[0]
	    
        contr[ind, 0, :, :, :] = temp1.data
        contr[ind, 1, :, :, :] = temp2.data
        #contr_best = contr.copy()
        #combained 3 best sensors for ttest
        # make np.array for 3 best sensors
        # condition 1
        best_chan1 = np.zeros((3, 20, 1350))
        
        for j, c in enumerate(best_chan_list):
            best_chan1[j] = temp1.data[c]
        
        # averaged data between 3 best sensors for conditions  1
        best_chan_mean1 = best_chan1.mean(axis = 0)
        # condition 2    
        best_chan2 = np.zeros((3, 20, 1350))
        
        for j, c in enumerate(best_chan_list):
            best_chan2[j] = temp2.data[c]            
            
        # averaged data between 3 best sensors for conditions  2     
        best_chan_mean2 = best_chan2.mean(axis = 0)
        
        # in contr_best we are interesting only in sensor 0 - in reallity this sensor in average data of 3 best sensors
        contr[ind, 0, 0, :, :] = best_chan_mean1
        contr[ind, 1, 0, :, :] = best_chan_mean2
            		        
	# 3 best sensors (only 0 sensor)
	
    comp1_best = contr[:, 0, :, :, :]
    comp2_best = contr[:, 1, :, :, :]
    t_stat, p_val = stats.ttest_rel(comp2_best, comp1_best, axis=0)

    comp1_mean_best = comp1_best.mean(axis=0)
    comp2_mean_best = comp2_best.mean(axis=0)
		
		
    return t_stat, p_val, comp1_mean_best, comp2_mean_best

def ttest_pair(data_path, subjects, parameter1, parameter2, freq_range, planar,fr, n): # n - количество временных отчетов
	contr = np.zeros((len(subjects), 2, 102, fr, n))

	for ind, subj in enumerate(subjects):
	    temp1 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_average_{2}_resp_{3}.h5'.format(subj, parameter1, freq_range, planar)))[0]
	    temp2 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_average_{2}_resp_{3}.h5'.format(subj, parameter2, freq_range, planar)))[0]
	    
	    contr[ind, 0, :, :, :] = temp1.data
	    contr[ind, 1, :, :, :] = temp2.data
        		        
		
	comp1 = contr[:, 0, :, :, :]
	comp2 = contr[:, 1, :, :, :]
	t_stat, p_val = stats.ttest_rel(comp2, comp1, axis=0)

	comp1_mean = comp1.mean(axis=0)
	comp2_mean = comp2.mean(axis=0)
	
	return t_stat, p_val, comp1_mean, comp2_mean

#############################################################################
##################### непарный ttest #######################################	
def ttest_vs_zero(data_path, subjects, parameter1, freq_range, planar, fr, n): # n - количество временных отчетов
	contr = np.zeros((len(subjects), 1, 102, fr, n))

	for ind, subj in enumerate(subjects):
		temp1 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_average_{2}_resp_{3}.h5'.format(subj, parameter1, freq_range, planar)))[0]
		
		contr[ind, 0, :, :, :] = temp1.data
				
	comp1 = contr[:, 0, :, :, :]
	t_stat, p_val = stats.ttest_1samp(comp1, 0, axis=0)

	comp1_mean = comp1.mean(axis=0)
		
	return t_stat, p_val, comp1_mean

def ttest_vs_zero_comb_channels(data_path, subjects, parameter1, freq_range, planar, fr, n, best_chan_list): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 102, fr, n))

    for ind, subj in enumerate(subjects):
        temp1 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_average_{2}_resp_{3}.h5'. format(subj, parameter1, freq_range, planar)))[0]
		
        contr[ind, :, :, :] = temp1.data
        		
        #combained 3 best sensors for ttest
        # make np.array for 3 best sensors

        best_chan1 = np.zeros((3, 20, 1350))
        
        for j, c in enumerate(best_chan_list):
            best_chan1[j] = temp1.data[c]
        
        # averaged data between 3 best sensors for conditions  1
        best_chan_mean1 = best_chan1.mean(axis = 0)
                
        # in contr_best we are interesting only in sensor 0 - in reallity this sensor in average data of 3 best sensors
        contr[ind, 0, :, :] = best_chan_mean1
        
            		        
	# 3 best sensors (only 0 sensor)
    #comp1_best = contr_best[:, 0, :, :, :]
    t_stat, p_val = stats.ttest_1samp(contr, 0, axis=0)

    comp1_mean_best = contr.mean(axis=0)
		
    return t_stat, p_val, comp1_mean_best

###################### строим topomaps со статистикой, для разницы между условиями #########################
# donor creation see make_donor_for_tfr_plot.ipynb
# mean1, mean2 - tfr average between subjects (see def ttest_pair)

def plot_deff_tf_comb_channels(p_val, donor, mean1, mean2, folder_out, treshold = 0.05): 	
    
	
    donor.data = mean2 - mean1
    b = donor.plot([0], baseline=None, tmin=-1.5, tmax=2.5, vmin=-2.0, vmax=2.0, title='Three best sensors averaged', show = False);
    b_stat = donor.plot([0], baseline=None, tmin=-1.5, tmax=2.5, vmin=-2.0, vmax=2.0, title='Three best sensors averaged', mask = p_val[0] < treshold, mask_style = 'contour', show = False);
    	
    
    return b, b_stat   
    
def plot_deff_tf_comb_channels_without_stat(p_val, donor, mean1, mean2, folder_out, best_chan_list):

    donor.data = mean2 - mean1
    best_chan = np.zeros((3, 20, 1350))
    for ind, c in enumerate(best_chan_list):
        best_chan[ind] = donor.data[c]

    best_chan_mean = best_chan.mean(axis = 0)
    
    donor.data[0] = best_chan_mean

    b = donor.plot([0], baseline=None, tmin=-1.5, tmax=2.5, vmin=-2.0, vmax=2.0, title='Three best sensors averaged, without stat', show = False);   
    
    return b
    
def plot_deff_tf(p_val, donor, mean1, mean2, folder_out, title, treshold = 0.05): 	
    
	
    donor.data = mean2 - mean1
    
    fig = donor.plot(baseline=None, mode='logratio', title=title, combine = 'mean', mask = p_val.mean(axis = 0 ) < treshold, mask_style = 'contour', show = False);
    
    # получаем отдельную картинку для каждого канала
    for chan in range(len(donor.ch_names)):
	    b = donor.plot([chan], baseline=None, title=donor.ch_names[chan], mask = p_val[chan] < treshold, mask_style = 'contour', show = False);
	    name = '/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/'.format(folder_out) + donor.ch_names[chan] + '.jpeg'
	    b[0].savefig(name, dpi=300, format='jpeg', transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
	
    
    return fig   

###################### строим topomaps со статистикой, для разницы между условиями #########################

def plot_tf_vs_zero(p_val, donor, mean1, folder_out, title, treshold = 0.05): 	

    donor.data = mean1

    fig = donor.plot(baseline=None, mode='logratio', title=title, combine = 'mean', mask = p_val.mean(axis = 0 ) < treshold, mask_style = 'contour', show = False);
    
    # получаем отдельную картинку для каждого канала
    for chan in range(len(donor.ch_names)):
	    b = donor.plot([chan], baseline=None, title=donor.ch_names[chan], mask = p_val[chan] < treshold, mask_style = 'contour', show = False);
	    name = '/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/'.format(folder_out) + donor.ch_names[chan] + '.jpeg'
	    b[0].savefig(name, dpi=300, format='jpeg', transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)



    return fig   

def plot_tf_vs_zero_comb_channels(p_val, donor, mean1, folder_out, treshold = 0.05): 	

    donor.data = mean1
    
    b = donor.plot([0], baseline=None, tmin=-1.5, tmax=2.5, vmin=-4, vmax=4, title='Three best sensors averaged', show = False);
    b_stat = donor.plot([0], baseline=None, tmin=-1.5, tmax=2.5, vmin=-4, vmax=4, title='Three best sensors averaged', mask = p_val[0] < treshold, mask_style = 'contour', show = False);
    
    return b, b_stat
    
def plot_tf_vs_zero_comb_channels_without_stat(p_val, donor, mean1, folder_out, best_chan_list): 	    
    
    donor.data = mean1
    best_chan = np.zeros((3, 20, 1350))
    for ind, c in enumerate(best_chan_list):
        best_chan[ind] = donor.data[c]

    best_chan_mean = best_chan.mean(axis = 0)
    
    donor.data[0] = best_chan_mean

    b = donor.plot([0], baseline=None, tmin=-1.5, tmax=2.5, vmin=-4, vmax=4, title='Three best sensors averaged, without stat', show = False);   
    
    return b    
      
######################## функция для смены имени файла с TF plots для отдельного сенсора ###################

def name_comb_planar(old_name):
    # разделяем строку по букве G (как в MEG0632.jpeg)
    b = re.split('G+', old_name)
    # получаем список из двух элементов берем 2ой, там где цифры и разделяем по точке, чтобы разделить разширение
    c = b[1].split(".")
    # берем первый элемент, где только цифры и делаем из них список, а затем делаем их числами (int())
    result = list(c[0])
    integer = []
    for i in result:
        integer.append(int(i))
        
    # увеличиваем четвертый элемент на 1 и убераем ненужный пятый (образовался при добавлении)
    integer.insert(3, (integer[3]+1))
    integer.pop()
    #Обратная операция - складываем все элементы в строку    
    string = []
    for i in integer:
        string.append(str(i))     
    string.insert(0, '+')
    myString = ''.join(string)
    d = old_name.split(".")
    d.insert(1, myString)
    d.insert(2, '.')
    new_name = ''.join(d)
    
    return(new_name)

##########################################################
#################### Рисование ###########################

# Очищаем pdf документ
def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

# функция, чтобы добавить текст (текстовое значение) в html документ
def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

#преобразование данных в mat-файле в текстовые значения
def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp


# добавление рисунка на экран
# filename - название html файла в который мы будем размещать картинку
# pic - название картинки
# pic_folder - откуда берем картинку
# pos_n - позиция
# size - размер

def add_pic_html(filename, pic, pic_folder, pos_n, size):
    x = size[0]
    y = size[1]
    add_str_html(filename, '<IMG STYLE="position:absolute; TOP: %spx; LEFT: %spx; WIDTH: %spx; HEIGHT: %spx" SRC= %s />'%(round(y*(1-pos_n[1])*15,3), round(pos_n[0]*x*15,3), x, y, pic_folder+'/'+pic))

