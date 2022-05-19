import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul

#################################################################################
#######################################################################################################################
#################### make stc with **source_band_induced_power**, but substituting the epochs into the function one at time ##################
#################### normalization to baseline only with noise covariance matrix #############################################################

def make_stc_epochs(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, bem, src, events, events_response, trans):

    bands = dict(beta=[L_freq, H_freq])
    #freqs = np.arange(L_freq, H_freq, f_step)
    

    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
        
    
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		    
	# Forward Model
    #trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/{0}-COR.fif'.format(subj)
        
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs_bl = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    cov = mne.compute_covariance(epochs=epochs_bl, method='auto', tmin=-0.35, tmax = -0.05)
     
    #epochs_bl.resample(100)
    
    ####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)


                
    fwd = mne.make_forward_solution(info=epochs.info, trans=trans, src=src, bem=bem)	                
    inv = mne.minimum_norm.make_inverse_operator(raw_data.info, fwd, cov, loose=0.2) 	                
		       
    epochs.resample(100) 

    stc_epo_list = []
    for ix in range(len(epochs)):
        stc = mne.minimum_norm.source_band_induced_power(epochs[ix].pick('meg'), inv, bands, method='sLORETA', use_fft=False, df = f_step, n_cycles = 8)["beta"]
        
        #data = 10*np.log10(stc.data) # make log transformation
        #stc.data = 10*np.log10(stc.data/b_line[:, np.newaxis])
        #stc.data = data
        stc_epo_list.append(stc)
    return (stc_epo_list)

