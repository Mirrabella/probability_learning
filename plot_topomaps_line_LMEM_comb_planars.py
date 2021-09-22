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


freq_range = 'beta_16_30_trf_early_log'
# создадим папку, куда будем сохранять рисунки
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/topomaps_LMEM'.format(freq_range), exist_ok = True)

# загружаем таблицу с pvalue, полученными с помощью LMEM в R
df = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/dataframe_for_LMEM_{0}/p_values_LMEM/p_vals_Tukey_by_trial_type_MEG_beta_16_30_el.csv'.format(freq_range))



# загружаем комбайн планары, усредненные внутри каждого испытуемого
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/{0}_comb_planar'.format(freq_range)

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

'''
# у следующих испытуемых риски удалились после коррекции меток (удаления технических артефактов и восставновления недостающих (Лера)). У этих испытуемых "Риски" были повторными, а мы брали, только одиночные
subjects.remove('P005')
subjects.remove('P037')
subjects.remove('P061')

'''
  
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


# задаем время и донора
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

########################### norisk vs risk ##############################
_, _, risk_mean, norisk_mean = ttest_pair(data_path, subjects, parameter1 = 'risk', parameter2 = 'norisk', freq_range = freq_range, planar = 'comb_planar', n = n)


########################### p value #############################

pval_in_intevals = []
# number of heads in line and the number of intervals into which we divided (see amount of tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_norisk_risk = pval_s['norisk_risk'].tolist()
    pval_in_intevals.append(pval_norisk_risk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

# считаем разницу бета и добавляем к шаблону (донору)
temp.data = risk_mean - norisk_mean

# время в которое будет строиться топомапы
times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])

# интервалы усредения
tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]

data_for_plotting = np.empty((102, 0))

#усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения

for i in range(17):
    data_in_interval = temp.copy()
    data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
    data_mean = data_in_interval.data.mean(axis = 1)
    data_mean = data_mean.reshape(102,1)
    data_for_plotting = np.hstack([data_for_plotting, data_mean])

plotting_LMEM = mne.EvokedArray(data_for_plotting, info = temp.info)
plotting_LMEM.times = times

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'norisk vs risk, LMEM, noFDR'
fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'norisk vs risk, LMEM,  space FDR'
fig2 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'norisk vs risk, LMEM, full FDR'
fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))



fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/topomaps_LMEM/LMEM_norisk_vs_risk_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/topomaps_LMEM/LMEM_norisk_vs_risk_stat_space_fdr.jpeg'.format(freq_range), dpi = 300)


fig3.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/topomaps_LMEM/LMEM_norisk_vs_risk_stat_full_fdr.jpeg'.format(freq_range), dpi = 300)



#print(len(pval_in_intevals))


########################### norisk vs prerisk ##############################
_, _, prerisk_mean, norisk_mean = ttest_pair(data_path, subjects, parameter1 = 'prerisk', parameter2 = 'norisk', freq_range = freq_range, planar = 'comb_planar', n = n)


########################### p value #############################

pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_norisk_prerisk = pval_s['norisk_prerisk'].tolist()
    pval_in_intevals.append(pval_norisk_prerisk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

# считаем разницу бета и добавляем к шаблону (донору)
temp.data = prerisk_mean - norisk_mean

# время в которое будет строиться топомапы
times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])

# интервалы усредения
tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]

data_for_plotting = np.empty((102, 0))

#усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения

for i in range(17):
    data_in_interval = temp.copy()
    data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
    data_mean = data_in_interval.data.mean(axis = 1)
    data_mean = data_mean.reshape(102,1)
    data_for_plotting = np.hstack([data_for_plotting, data_mean])

plotting_LMEM = mne.EvokedArray(data_for_plotting, info = temp.info)
plotting_LMEM.times = times

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'norisk vs prerisk, LMEM, noFDR'
fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'norisk vs prerisk, LMEM,  space FDR'
fig2 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'norisk vs prerisk, LMEM, full FDR'
fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))



fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/topomaps_LMEM/LMEM_norisk_vs_prerisk_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/topomaps_LMEM/LMEM_norisk_vs_prerisk_stat_space_fdr.jpeg'.format(freq_range), dpi = 300)


fig3.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{0}/topomaps_LMEM/LMEM_norisk_vs_prerisk_stat_full_fdr.jpeg'.format(freq_range), dpi = 300)



#print(len(pval_in_intevals))



