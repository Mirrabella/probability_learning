#!/usr/bin/env python
# coding: utf-8

import mne
import os
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
from mne.preprocessing import ICA
from mne.preprocessing import create_eog_epochs, create_ecg_epochs
from cleaning_raw_ica import cleaning_raw_ica
import param

# choose data path to download raw files for cleaning. This path for two days learn speech experiment
data_path = '/net/server/data/Archive/prob_learn/experiment'

# you can change all parametrs in param.py
subjects =param.subjects 
rounds = param.rounds
date = param.date

for idx, subj in enumerate(subjects):
	#make a folder where you ica solutions will be save. Don't forget change path.
	os.makedirs(op.join('/home/vtretyakova/Desktop/prob_learned/ICA_cleaning_pl/properties/', '{0}'.format(subj)), exist_ok=True)
	for r in rounds:
		raw_name = '{0}/{1}/ORIGINAL_TSSS/{0}_run{2}_raw_tsss_mc.fif'.format(subj, date[idx], r)
		raw_file = op.join(data_path, raw_name)
		raw = mne.io.Raw(raw_file, preload=True)
		rank = mne.compute_rank(raw, rank='info')
		rank = int(rank['meg']) # rank is use as a number of components in ica analisis
	
		#more information about cleaning_raw_ica see in cleaning_raw_ica.py
		ica = cleaning_raw_ica (subj=subj, raw = raw, n_components = rank, r = r, method = 'fastica', decim = 3)
		#don't forget to change path
		ica.save('/home/vtretyakova/Desktop/prob_learned/ICA_cleaning_pl/properties/{0}/{1}_{0}-ica.fif'.format(subj, r))

