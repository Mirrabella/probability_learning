#https://mne.tools/dev/auto_examples/stats/plot_fdr_stats_evoked.html#sphx-glr-auto-examples-stats-plot-fdr-stats-evoked-py

import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_fb_ave_separ_comb_planar'

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

# задаем планары
# planars = ['planar1', 'planar2', 'comb_planar']
planars = ['planar1', 'planar2']

	##### 1. norisk - risk #####
######### 1.1 контраст norisk vs 0, without correction #########################
for p in planars:	
    t_stat_norisk, p_val_norisk, norisk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'norisk', planar = p, n = n)
    title = ('norisk vs zero %s, no FDR'%p)
    fig, temp = plot_topo_vs_zero(p_val_norisk, temp, norisk_mean, time_to_plot, title)

    fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_0_stat_no_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)

    temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/norisk_vs_0_{0}_separ_fb.fif'.format(p))  # save evoked data to disk

######### 1.2 контраст risk vs 0, without correction #########################
for p in planars:	
    t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'risk', planar = p, n = n)

    fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = ('norisk vs zero %s, no FDR'%p))

    fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/risk_vs_0_stat_no_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)

    temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/risk_vs_0_{0}_separ_fb.fif'.format(p))  # save evoked data to disk

######### 1.3 контраст norisk vs risk, without correction #########################
for p in planars:
    t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, subjects, parameter1 = 'risk', parameter2 = 'norisk', planar = p, n = n)

    _, fig2, temp = plot_deff_topo(p_val, temp, norisk_mean, risk_mean, time_to_plot, title = ('norisk vs risk %s, no FDR'%p))

    fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_risk_stat_no_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)

    temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/norisk_vs_risk_{0}_separ_fb.fif'.format(p))  # save evoked data to disk

    ######### 1.4 контраст norisk vs risk, with space fdr correction #########################

    p_val_space_fdr = space_fdr(p_val)

    _, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, risk_mean, time_to_plot, title = ('norisk vs risk %s, space FDR'%p))

    fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_risk_stat_space_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)



    ######### 1.5 контраст norisk vs risk, with full fdr correction #########################

    p_val_full_fdr = full_fdr(p_val)

    _, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, risk_mean, time_to_plot, title = ('norisk vs risk %s, full FDR'%p))

    fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_risk_stat_full_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)



	##### 2. norisk - prerisk #####

######### 2.1 контраст norisk vs 0, without correction #########################
for p in planars:	
    t_stat_norisk, p_val_norisk, norisk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'norisk', planar = p, n = n)

    fig, temp = plot_topo_vs_zero(p_val_norisk, temp, norisk_mean, time_to_plot, title = ('norisk vs zero %s, no FDR'%p))

    fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_0_stat_no_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)

######### 2.2 контраст prerisk vs 0, without correction #########################
for p in planars:	
    t_stat_prerisk, p_val_prerisk, prerisk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'prerisk', planar = p, n = n)

    fig, temp = plot_topo_vs_zero(p_val_prerisk, temp, prerisk_mean, time_to_plot, title = ('prerisk vs zero %s, no FDR'%p))

    fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/prerisk_vs_0_stat_no_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)

    temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/prerisk_vs_0_{0}_separ_fb.fif'.format(p))  # save evoked data to disk

######### 2.3 контраст norisk vs prerisk, without correction #########################
for p in planars:
    t_stat, p_val, prerisk_mean, norisk_mean = ttest_pair(data_path, subjects, parameter1 = 'prerisk', parameter2 = 'norisk', planar = p, n = n)

    _, fig2, temp = plot_deff_topo(p_val, temp, norisk_mean, prerisk_mean, time_to_plot, title = ('norisk vs prerisk %s, no FDR'%p))

    fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_prerisk_stat_no_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)

    temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/norisk_vs_prerisk_{0}_separ_fb.fif'.format(p))  # save evoked data to disk

    ######### 2.4 контраст norisk vs prerisk, with space fdr correction #########################

    p_val_space_fdr = space_fdr(p_val)

    _, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, prerisk_mean, time_to_plot, title = ('norisk vs prerisk %s, space FDR'%p))

    fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_prerisk_stat_space_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)



    ######### 2.5 контраст norisk vs prerisk, with full fdr correction #########################

    p_val_full_fdr = full_fdr(p_val)

    _, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, prerisk_mean, time_to_plot, title = ('norisk vs prerisk %s, full FDR'%p))

    fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_prerisk_stat_full_fdr_{0}_separ_fb.jpeg'.format(p), dpi = 300)



