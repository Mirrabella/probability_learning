#!/usr/bin/env python
# coding: utf-8

import mne
import os
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from mne.preprocessing import ICA
from mne.preprocessing import create_eog_epochs, create_ecg_epochs

# r - round
def cleaning_raw_ica (subj, raw, n_components, r, method = 'fastica', decim = 3):
	#choose only meg picks
	picks_meg = mne.pick_types(raw.info, meg=True, eeg=False, eog=False, stim=False, exclude=[])

	#find events for horisontal eyes movements (ch_name is name of channel in your exmeriment)
	eog_events_h = mne.preprocessing.find_eog_events(raw, event_id=998, ch_name='MISC302') 

	#find events for vertical eyes movements (ch_name is name of channel in your exmeriment)
	eog_events_v = mne.preprocessing.find_eog_events(raw, event_id=997, ch_name='MISC301') 
	
	#find events for heat beats (ch_name is name of channel in your exmeriment)
	#find_ecg_events return events and average pulse, so you take only [0] elements
	ecg_events = mne.preprocessing.find_ecg_events(raw, event_id=999, ch_name='ECG063')[0]
	
	#select the frequency range you are intrested in
	raw.filter(0.1, 200., fir_design='firwin')

	#Removing power-line noise with notch filtering
	raw.notch_filter(np.arange(50, 201, 50), picks=picks_meg, filter_length='auto', phase='zero')

	ica = ICA(n_components=n_components, method=method, allow_ref_meg=False)
	reject = dict(mag=9e-12, grad=4e-10) #Alexandra Razorenova conspect.
	ica.fit(raw, picks=None)
	print(ica)
	
	#epochs for horizontal eyes movements
	eog_epochs_h = create_eog_epochs(raw, ch_name='MISC302', event_id=998)  
	eog_inds_h, scores_h = ica.find_bads_eog(eog_epochs_h, ch_name='MISC302', threshold=5.0)  
	

	try:
		properties_h = ica.plot_properties(eog_epochs_h, picks=eog_inds_h, psd_args={'fmax': 35.}, image_args={'sigma': 1.}, show=False)
		for id, p in enumerate(properties_h):
			p.savefig('/home/vtretyakova/Desktop/prob_learned/ICA_cleaning_pl/properties/{0}/{1}_{0}_prop_horiz_{2}.jpeg'.format(subj, r, ica.labels_['eog/0/MISC302'][id]))
	except ValueError:
		print ('No appropriate channels found for the given picks ([])') 
	
	#epochs for vertical eyes movements
	eog_epochs_v = create_eog_epochs(raw, ch_name='MISC301', event_id=997)  
	eog_inds_v, scores_v = ica.find_bads_eog(eog_epochs_v, ch_name='MISC301', threshold=5.0)  
	
	try:
		properties_v = ica.plot_properties(eog_epochs_v, picks=eog_inds_v, psd_args={'fmax': 35.}, image_args={'sigma': 1.}, show=False)
		for id, p in enumerate(properties_v):
			p.savefig('/home/vtretyakova/Desktop/prob_learned/ICA_cleaning_pl/properties/{0}/{1}_{0}_ica_prop_vert_{2}.jpeg'.format(subj, r, ica.labels_['eog/0/MISC301'][id]))
	except ValueError:
		print ('No appropriate channels found for the given picks ([])')

 	
	#epochs for heart beats
	ecg_epochs = create_ecg_epochs(raw, tmin=-.5, tmax=.5)
	ecg_inds, scores = ica.find_bads_ecg(ecg_epochs, method='ctps')
	print(ica.labels_)
	
	try:
		properties_ecg = ica.plot_properties(ecg_epochs, picks=ecg_inds, psd_args={'fmax': 35.}, show=False);
		for id, p in enumerate(properties_ecg):
			p.savefig('/home/vtretyakova/Desktop/prob_learned/ICA_cleaning_pl/properties/{0}/{1}_{0}_ica_prop_ecg_{2}.jpeg'.format(subj, r, ica.labels_['ecg'][id]))
	except ValueError:
		print ('No appropriate channels found for the given picks ([])')
	
	#if you already know with components you will drop you can use following code.
	'''
	eog_comp = ica.labels_['eog/0/EOG061']
	ecg_comp = ica.labels_['ecg']
	comp_drop = eog_comp + ecg_comp
	raw_ica = raw.copy()
	ica.apply(raw_ica, exclude = comp_drop)
	raw_ica.save('/home/vtretyakova/Desktop/New_experiment/active1/{0}_raw_ica_d1a1.fif'.format(subj), overwrite=True)
	'''
	#Otherwise, select the components to substract from resulting figures of the components properties and the use drop_components.py


	return(ica)
