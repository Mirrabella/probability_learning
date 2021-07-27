

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

	# Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(freq_show_baseline.data, 0, 1)
    b_line = np.swapaxes(b_line, 1, 2)
	
	# выстраиваем в ряд бейзлайны для каждого из эвентов, как будто они происходили один за другим
    a, b, c, d = b_line.shape
    b_line = b_line.reshape(a, b, c * d)

	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		       
    epochs.resample(300) 

    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, use_fft = False, return_itc = False, average=False)
	
	####### Для данных так же меняем оси местами
    data = np.swapaxes(freq_show.data, 0, 1)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 2, 3)
	
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1)
    b_line_new_shape = b[:, :, np.newaxis, np.newaxis]

    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 2, 3)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    
    freq_show.data = data
    
    return (freq_show)


# функция для смены имени файла с TF plots для отдельного сенсора
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







