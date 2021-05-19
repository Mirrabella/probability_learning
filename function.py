import mne
import os
import os.path as op
import numpy as np
import pandas as pd



# File with events was made by Lera, you need this function for reading it
def read_events(filename):
    with open(filename, "r") as f:
        b = f.read().replace("[","").replace("]", "").replace("'", "")
        b = b.split("\n")
        b = list(map(str.split, b))
        b = list(map(lambda x: list(map(int, x)), b))
        return np.array(b[:])

# Функция для поиска меток фиксационного креста (по ним ищется baseline)
def fixation_cross_events(data_path_raw, raw_name, data_path_events, name_events, subj, r, fb):
    
    # для чтения файлов с events используйте либо np.loadtxt либо read_events
    no_risk = np.loadtxt(op.join(data_path_events, name_events.format(subj, r, fb)), dtype='int')
        
    #no_risk = read_events(op.join(data_path_events, name_events.format(subj, r)))
    
    # Load raw event with miocorection
    events_raw = read_events(op.join(data_path_raw, raw_name.format(subj, r)))        
    # Load data

    #raw_fname = op.join(data_path_raw, raw_name.format(subj, r))

    #raw = mne.io.Raw(raw_fname, preload=True)

    #events_raw = mne.find_events(raw, stim_channel='STI101', output='onset', 
    #                                 consecutive='increasing', min_duration=0, shortest_event=1, mask=None, 
    #                                 uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    
    if no_risk.shape == (3,):
        no_risk = no_risk.reshape(1,3)
    # список индексов трайлов
    x = []
    for i in range(len(events_raw)):
	    for j in range(len(no_risk)):
		    if np.all((events_raw[i] - no_risk[j] == 0)):
			    x+=[i]

    x1 = 1 #fixation cross

    full_ev = []
    for i in x:
        full_ev += [list(events_raw[i])] # список из 3ех значений время х 0 х метка
        j = i - 1
        ok = True      
        while ok:
            full_ev += [list(events_raw[j])]
            if events_raw[j][2] == x1:
                ok = False
            j -= 1 

                
    event_fixation_cross_norisk = []

    for i in full_ev:
        if i[2] == x1:
            event_fixation_cross_norisk.append(i)
                    
    event_fixation_cross_norisk = np.array(event_fixation_cross_norisk)
     
    return(event_fixation_cross_norisk)


# Функция для получения эпохированных tfr сингл трайлс
def make_beta_signal(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline):
    freqs = np.arange(L_freq, H_freq, f_step)
    
    #read events
	#events for baseline
    events = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_{2}_fix_cross.txt".format(subj, r, fb), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events.shape == (3,):
        events = events.reshape(1,3) 
    
    
    #events, which we need
    events_response = np.loadtxt('/net/server/data/Archive/prob_learn/ksayfulina/events_clean_after_mio/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_response.shape == (3,):
        events_response = events_response.reshape(1,3)
    
	           
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
        
    
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		    
	   	    
    #epochs for baseline
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, picks = picks, preload = True)
    epochs.resample(300)

    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	    
        #add up all values according to the frequency axis
    b_line = freq_show_baseline.data.sum(axis=-2)
	    
	    # Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
        
        # выстраиваем в ряд бейзлайны для каждого из 28 эвентов, как будто они происходили один за другим
    a, b, c = b_line.shape
    b_line = b_line.reshape(a, b * c)
	    

	####### ДЛЯ ДАННЫХ ##############

    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, picks = picks, preload = True)
		       
    epochs.resample(300) 

    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False)

    temp = freq_show.data.sum(axis=2)
	    
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
        
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
        
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
        
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = -1.750, events = events_response)
        
    return (epochs_tfr)   
        
# Фукнция для получения предыдущего фидбека
def prev_feedback(events_raw, tials_of_interest, FB):
    
    #Получаем индексы трайлов, которые нас интересуют
    
    x = []
    for i in range(len(events_raw)):
	    for j in range(len(tials_of_interest)):
		    if np.all((events_raw[i] - tials_of_interest[j] == 0)):
			    x+=[i]
    
    prev_fb = []

    for i in x:
        ok = True
        while ok:
            #print(i)
            if events_raw[i-1][2] in FB:
                a = events_raw[i-1].tolist()
                prev_fb.append(a)
                ok = False
            else:
                pass
            i = i - 1
            
    prev_fb = np.array(prev_fb)
    
    return(prev_fb)
    
    
    
def combine_planar_Epoches_TFR(EpochsTFR, tmin):
	ep_TFR_planar1 = EpochsTFR.copy(); 
	ep_TFR_planar2 = EpochsTFR.copy()
	ep_TFR_planar1.pick_types(meg='planar1')
	ep_TFR_planar2.pick_types(meg='planar2')

	#grad_RMS = np.power((np.power(evk_planar1.data, 2) + np.power(evk_planar2.data, 2)), 1/2)
	combine = ep_TFR_planar1.get_data() + ep_TFR_planar2.get_data()
	ep_TFR_combined = mne.EpochsArray(combine, ep_TFR_planar1.info, tmin = tmin, events = EpochsTFR.events)

	return ep_TFR_combined
	
    
def make_subjects_df(combined_planar, s, subj, r, t, fb_cur, tmin, tmax, scheme):

    combined_planar_in_interval = combined_planar.crop(tmin=tmin, tmax=tmax, include_tmax=True)

    mean_combined_planar = combined_planar_in_interval.get_data().mean(axis=-1)
    
    beta_power = []
beta_power
    for i in range(len(mean_combined_planar)):
        a = mean_combined_planar[i][s]
        beta_power.append(a)
    
    trial_number = range(len(mean_combined_planar))
    
    subject = [subj]*len(mean_combined_planar)
    run = ['run{0}'.format(r)]*len(mean_combined_planar)
    trial_type = [t]*len(mean_combined_planar)
    feedback_cur = [fb_cur]*len(mean_combined_planar)
    
    feedback_prev_data = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/prev_fb_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}_prev_fb.txt".format(subj, r, t, fb_cur), dtype='int')
    if feedback_prev_data.shape == (3,):
        feedback_prev_data = feedback_prev_data.reshape(1,3)
    
    FB_rew = [50, 51]
    FB_lose = [52, 53]

    feedback_prev = []
    for i in feedback_prev_data:
        if i[2] in FB_rew:
            a = 'positive'
            
        else:
            a = 'negative'
            
        feedback_prev.append(a)   
        
    # схема подкрепления   
    a = scheme.loc[(scheme['fname'] == subj) & (scheme['block'] == r)]['scheme'].tolist()[0]
    sch = [a]*len(mean_combined_planar)    
    
    
    df = pd.DataFrame()

    df['trial_number'] = trial_number
    df['beta_power'] = beta_power
    df['subject'] = subject
    df['round'] = run
    df['trial_type'] = trial_type
    df['feedback_cur'] = feedback_cur
    df['feedback_prev'] = feedback_prev
    df['scheme'] = sch
        
    return (df)
    
   
    
    
            
        

