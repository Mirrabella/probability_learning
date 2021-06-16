# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero, nocolor_topomaps_line

# загружаем таблицу с pvalue, полученными с помощью LMEM в R
df  = pd.read_csv('/net/server/data/Archive/prob_learn/ksayfulina/p_values_LMEM/p_vals_factor_significance_MEG.csv')

# задаем время для построения топомапов (используется в функции MNE plot_topomap)
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
# загружаем донора (любой Evoked с комбинированными планарами или одним планаром - чтобы было 102 сеносора). 
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = 17 # количество говов в ряду

# задаем временные точнки, в которых будем строить головы, затем мы присвоим их для донора (template)
times_array = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])


##############  empty topomaps line (without color) ##################

temp = nocolor_topomaps_line(n, temp, times_array)

############### 1. feedback_cur #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_norisk_prerisk = pval_s['feedback_cur'].tolist()
    pval_in_intevals.append(pval_norisk_prerisk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'feedback_cur, LMEM, noFDR'
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'feedback_cur, LMEM,  space FDR'
fig2 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'feedback_cur, LMEM, full FDR'
fig3 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))


fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_feedback_cur_stat_no_fdr.jpeg', dpi = 300)

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_feedback_cur_stat_space_fdr.jpeg', dpi = 300)

fig3.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_feedback_cur_stat_full_fdr.jpeg', dpi = 300)

############### 2. trial_type #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_norisk_prerisk = pval_s['trial_type'].tolist()
    pval_in_intevals.append(pval_norisk_prerisk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'trial_type, LMEM, noFDR'
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'trial_type, LMEM,  space FDR'
fig2 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'trial_type, LMEM, full FDR'
fig3 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))


fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_trial_type_stat_no_fdr.jpeg', dpi = 300)

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_trial_type_stat_space_fdr.jpeg', dpi = 300)

fig3.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_trial_type_stat_full_fdr.jpeg', dpi = 300)


############### 3. trial_type:feedback_cur #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_norisk_prerisk = pval_s['trial_type:feedback_cur'].tolist()
    pval_in_intevals.append(pval_norisk_prerisk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'trial_type:feedback_cur, LMEM, noFDR'
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'trial_type:feedback_cur, LMEM,  space FDR'
fig2 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'trial_type:feedback_cur, LMEM, full FDR'
fig3 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))


fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_trial_type_feedback_cur_stat_no_fdr.jpeg', dpi = 300)

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_trial_type_feedback_cur_stat_space_fdr.jpeg', dpi = 300)

fig3.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/signif_factors/LMEM_trial_type_feedback_cur_stat_full_fdr.jpeg', dpi = 300)


