#!/usr/bin/env python
# coding: utf-8

import mne
import os
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from mne.preprocessing import read_ica
import param

# you can change all parametrs in param.py
subjects =param.subjects 
#rounds = param.rounds
date = param.date
#run number
rounds = [1, 2, 3, 4, 5, 6]

#if you use main.py then you got figures of components properties,and select components for drop. Now you have to make list of lists, where each internal list refers to a specific subjects: for example components[0] - refers to L001, components[1] - refers to L002 and so on.
# Below is a list for an example (day2 move). You have to change it.
components = [[[3, 8, 9], [0, 7], [1, 0, 29], [0, 2], [0, 11], [0, 18], [0, 14], [0, 1, 25], [0, 2, 14], [0, 1, 2, 8], [1], [0, 2, 48], [0, 11], [0, 2, 4], [0, 1], [0], [0, 6], [0, 15], [0, 16]],
             [[1], [0, 1, 3, 6], [3, 1, 0, 26], [0, 2], [18], [0, 24], [0, 14], [0, 1], [0, 1, 5, 9], [0, 2, 16], [0, 25], [0, 3], [0, 3], [0, 12, 2, 3], [0, 2], [0], [0, 20], [0, 26], [0, 21]],
             [[1, 14], [0, 4], [18, 0, 42], [0, 3], [10], [0, 14], [0, 16, 18], [0, 2], [0, 7, 13], [0, 1, 13], [0, 53], [0, 2], [0, 3], [0, 1, 44], [0, 2], [0], [0, 16], [0, 17], [0, 9]], 
             [[1, 14, 16], [0, 4, 51], [3, 0, 33], [0, 5], [0, 7], [0, 16], [0, 39], [0, 3, 25], [0, 4, 10], [1, 12], [1], [0, 5, 54], [0], [0, 1, 43], [0, 2], [3], [0, 14], [0, 22], [0, 10, 24]], 
             [[1], [0, 4], [1, 0, 41], [1, 4], [2], [0, 22], [0, 11], [0, 3, 14], [0, 9, 14], [0, 2, 11], [1], [0, 8, 40], [0, 8], [0, 4, 17], [0, 1], [2, 36], [0, 12], [0, 20], [0, 19]],
             [[1], [0, 2], [4, 0, 41], [0, 4], [5, 9], [1, 2, 17], [0, 14], [0, 2, 14], [0, 2, 21], [0, 1, 9], [0], [0, 4, 7], [0, 13], [0, 1, 3], [0, 1], [2, 23], [0, 13], [0, 14], [0, 18]]
             ]

# choose data path to download raw files for cleaning. This path for two days learn speech experiment
data_path = '/net/server/data/Archive/prob_learn/experiment'


for i, r in enumerate(rounds):
	#make a dictionary - key is subject, list components for drop is object.
	comp_for_drop = dict(zip(subjects, components[i]))
	for idx, subj in enumerate(subjects):
		#make a folder where you want to save a result. Don't forget change path.
		os.makedirs(op.join('/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/', '{0}'.format(subj)), exist_ok=True)
		raw_name = '{0}/{1}/ORIGINAL_TSSS/{0}_run{2}_raw_tsss_mc.fif'.format(subj, date[idx], r)
		raw_file = op.join(data_path, raw_name)
		raw = mne.io.Raw(raw_file, preload=True)
	
		#select the frequency range you are intrested in, the same as in cleaning_raw_ica.py
		raw.filter(0.1, 200., fir_design='firwin')
		picks_meg = mne.pick_types(raw.info, meg=True, eeg=False, eog=False, stim=False, exclude=[])
	
		#Removing power-line noise with notch filtering
		raw.notch_filter(np.arange(50, 201, 50), picks=picks_meg, filter_length='auto', phase='zero')

		#read your ica solution. Don't forget specify the path where you saved it.
		ica = read_ica('/home/vtretyakova/Desktop/prob_learned/ICA_cleaning_pl/properties/{0}/{1}_{0}-ica.fif'.format(subj, r))
		raw_ica = raw.copy()

		ica.apply(raw_ica, exclude = comp_for_drop[subj])
		
		#don't forget to change path
		raw_ica.save('/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{0}/run{1}_{0}_raw_ica.fif'.format(subj, r), overwrite=False)	
