import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul




def make_freq_stc(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, bem, src):
    
    bands = dict(beta=[L_freq, H_freq])
    #freqs = np.arange(L_freq, H_freq, f_step)
    
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
		    
	# Forward Model
    trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/{0}-COR.fif'.format(subj)
        
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs_bl = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    cov = mne.compute_covariance(epochs=epochs_bl, method='auto', tmin=-0.35, tmax = -0.05)
     
    epochs_bl.resample(100)
    
    ####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)


                
    fwd = mne.make_forward_solution(info=epochs.info, trans=trans, src=src, bem=bem)	                
    inv = mne.minimum_norm.make_inverse_operator(raw_data.info, fwd, cov, loose=0.2) 	                
		       
    epochs.resample(100) 
    
    stc_baseline = mne.minimum_norm.source_band_induced_power(epochs_bl.pick('meg'), inv, bands, use_fft=False, df = f_step, n_cycles = 8)["beta"].crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True)
    
    
    #усредняем по времени
    b_line  = stc_baseline.data.mean(axis=-1)
    
    stc = mne.minimum_norm.source_band_induced_power(epochs.pick('meg'), inv, bands, use_fft=False, df = f_step, n_cycles = 8)["beta"]
    
    stc.data = 10*np.log10(stc.data/b_line[:, np.newaxis])
    # check beta power on norisk
    return (stc)
    #morph = mne.compute_source_morph(stc, subject_from=subj, subject_to='fsaverage')
    #stc_fsaverage = morph.apply(stc)

    #return (stc_fsaverage)
    
    
#######################################################################################################################
############################ first isolate frequency without average, than make stc for each epochs ##################

def make_stc_epochs_from_freq_epochs(subj, r, cond, fb, data_path, baseline, bem, src):

    #read events (for for inverse operator creation)
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
    
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)

    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs_bl = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    cov = mne.compute_covariance(epochs=epochs_bl, method='auto', tmin=baseline[0], tmax = baseline[1])
    
####### ДЛЯ ДАННЫХ ##############

    epochs_fname = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_epo/{0}_run{1}_{2}_fb_cur_{3}_beta_16_30_trf_early_log_epo.fif'.format(subj, r, cond, fb)
    
    epochs_beta = mne.read_epochs(epochs_fname, preload=True)
    
    # Forward Model
    trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/{0}-COR.fif'.format(subj)
    fwd = mne.make_forward_solution(info=epochs_beta.info, trans=trans, src=src, bem=bem)
    
    inv = mne.minimum_norm.make_inverse_operator(raw_data.info, fwd, cov, loose=0.2)  
    
    stc = mne.minimum_norm.apply_inverse_epochs(epochs_beta, inv, lambda2=1. / 9., pick_ori='normal')
    
    return (stc)
    
    
#######################################################################################################################
#################### make stc with **source_band_induced_power**, but substituting the epochs into the function one at time ##################

def make_stc_epochs_from_freq_epochs_var2(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, bem, src):

    bands = dict(beta=[L_freq, H_freq])
    #freqs = np.arange(L_freq, H_freq, f_step)
    
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
		    
	# Forward Model
    trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/{0}-COR.fif'.format(subj)
        
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs_bl = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    cov = mne.compute_covariance(epochs=epochs_bl, method='auto', tmin=-0.35, tmax = -0.05)
     
    epochs_bl.resample(100)
    
    ####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)


                
    fwd = mne.make_forward_solution(info=epochs.info, trans=trans, src=src, bem=bem)	                
    inv = mne.minimum_norm.make_inverse_operator(raw_data.info, fwd, cov, loose=0.2) 	                
		       
    epochs.resample(100) 
    
    stc_baseline = mne.minimum_norm.source_band_induced_power(epochs_bl.pick('meg'), inv, bands, use_fft=False, df = f_step, n_cycles = 8)["beta"].crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True)
    
    
    #усредняем по времени
    b_line  = stc_baseline.data.mean(axis=-1)
    b_line = 10*np.log10(b_line)
    
    stc_epo_list = []
    for ix in range(len(epochs)):
        stc = mne.minimum_norm.source_band_induced_power(epochs[ix].pick('meg'), inv, bands, use_fft=False, df = f_step, n_cycles = 8)["beta"]
        data = 10*np.log10(stc.data)
        #stc.data = 10*np.log10(stc.data/b_line[:, np.newaxis])
        stc.data = data - b_line[:, np.newaxis]
        stc_epo_list.append(stc)
    return (stc_epo_list)
    
#################################################################################


def make_inverse_operator(subj, r, cond, fb, data_path, baseline, period_start, period_end, bem, src):

    #read events (for for inverse operator creation)
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

    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs_bl = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    cov = mne.compute_covariance(epochs=epochs_bl, method='auto', tmin=baseline[0], tmax = baseline[1])
    
    
    ####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		                
    # Forward Model
    trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/{0}-COR.fif'.format(subj)
    fwd = mne.make_forward_solution(info=epochs.info, trans=trans, src=src, bem=bem)
    
    inv = mne.minimum_norm.make_inverse_operator(raw_data.info, fwd, cov, loose=0.2) 
    
    return (inv)
##################################################################3    
    
def signed_p_val(t, p_val):
    if t >= 0:
        return 1 - p_val
    else:
        return -(1 - p_val)   
