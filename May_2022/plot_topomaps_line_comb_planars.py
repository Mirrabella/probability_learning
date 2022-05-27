#https://mne.tools/dev/auto_examples/stats/plot_fdr_stats_evoked.html#sphx-glr-auto-examples-stats-plot-fdr-stats-evoked-py

import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar'

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]

# следующие испытуемы удаляются из выборки по причине возраста (>40 лет), либо нерискующие
subjects.remove('P000')
subjects.remove('P020')
subjects.remove('P036')
subjects.remove('P049')
subjects.remove('P056')


# у следующих испытуемых риски удалились после коррекции меток (удаления технических артефактов и восставновления недостающих (Лера)). У этих испытуемых "Риски" были повторными, а мы брали, только одиночные
subjects.remove('P005')
subjects.remove('P037')
subjects.remove('P061')


  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
cond_list = ['_norisk_fb_cur_positive',
             '_prerisk_fb_cur_positive',
             '_risk_fb_cur_positive',
             '_postrisk_fb_cur_positive',
             '_norisk_fb_cur_negative',
             '_prerisk_fb_cur_negative',
             '_risk_fb_cur_negative',
             '_postrisk_fb_cur_negative'
             ]

out_path='/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/' #path to epochs
f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


subj_list = subjects.copy()
for i,subject in enumerate(subjects):
    subject_files = [file for file in f if subject in file] #make list with all subject files 
    for j in cond_list: #check if subject has all conditions
        if not any(j in s for s in subject_files):
            if subject in subj_list:
                subj_list.remove(subject)

subjects = subj_list
print(len(subjects))


# 40 subjects with all choice types
'''
subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6
'''
# задаем время и донора
time_to_plot = np.linspace(-0.7, 2.5, num = 9)
#time_to_plot = np.linspace(-0.8, 2.4, num = 17)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/P001_norisk_evoked_beta_16_30_trf_early_log_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

freq_range = 'beta_16_30'
choice_types = ['norisk', 'risk', 'prerisk', 'postrisk']


for cht in choice_types:

    t_stat, p_val, mean = ttest_vs_zero(data_path, subjects, parameter1 = cht, freq_range = 'beta_16_30', planar = 'comb_planar', n = n)
    title = f'{cht} vs zero, no FDR'
    fig, temp = plot_topo_vs_zero(p_val, temp, mean, time_to_plot, title)

    fig.savefig('/home/vtretyakova/Рабочий стол/probability_learning/may_2022/topomaps_choice_type/subj_like_in_source/400ms_{0}_vs_0_stat_no_fdr_scale_4_5.jpeg'.format(cht), dpi = 300)

    #temp.save('/home/vtretyakova/Рабочий стол/probability_learning/may_2022/topomaps_choice_type/{0}_vs_0_1_7.fif'.format(cht))  # save evoked data to disk


##################################### average all choice types #############################
'''
all_array = np.zeros(shape=(4, 102, n))
for i, cht in enumerate(choice_types):
    fif = mne.Evoked('/home/vtretyakova/Рабочий стол/probability_learning/may_2022/topomaps_choice_type/norisk_vs_0.fif')
    all_array[i, :, :] = fif.data
print(all_array.shape)

mean = all_array.mean(axis=0)

temp.data = mean
#temp.save('/home/vtretyakova/Рабочий стол/probability_learning/may_2022/topomaps_choice_type/all_choice_types.fif'.format(cht))  # save evoked data to disk
title = 'all choice types'
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, average=0.4, units = 'dB', show = False, vmin = -4.5, vmax = 4.5, time_unit='s', title = title, colorbar = True, extrapolate = "local")
fig.savefig('/home/vtretyakova/Рабочий стол/probability_learning/may_2022/topomaps_choice_type/400ms_all_choice_types_scale_4_5.jpeg'.format(cht), dpi = 300)
'''



