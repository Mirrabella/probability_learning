
import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from functions import ttest_pair, ttest_vs_zero, plot_deff_tf, plot_tf_vs_zero


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

# донор (donor creation see make_donor_for_tfr_plot.ipynb)
donor = mne.time_frequency.read_tfrs('/home/vtretyakova/Рабочий стол/time_frequency_plots/donor_evoked_combined_planars.h5', condition=None)[0]

os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels', exist_ok = True)

############# 1. риск против нериска #########################################
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_40_comb_planars/comb_planars_average_betwee_fb'


os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/norisk_vs_risk', exist_ok = True)
folder_out = 'norisk_vs_risk'

p1 = 'norisk'
p2 = 'risk'


_, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, 'comb_planar', n = 1350)

fig = plot_deff_tf(p_val, donor, mean1, mean2, folder_out, title = "Average channel {0} vs {1}".format(p1, p2), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_vs_norisk_stat_no_fdr.jpeg', dpi = 300)

############# 2. прериск против нериска #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/norisk_vs_prerisk', exist_ok = True)
folder_out = 'norisk_vs_prerisk'


p1 = 'norisk'
p2 = 'prerisk'

_, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, 'comb_planar', n = 1350)

fig = plot_deff_tf(p_val, donor, mean1, mean2, folder_out, title = "Average channel {0} vs {1}".format(p1, p2), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/prerisk_vs_norisk_stat_no_fdr.jpeg', dpi = 300)

############# 3. риск против 0 #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/risk_vs_0', exist_ok = True)
folder_out = 'risk_vs_0'

p1 = 'risk'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, 'comb_planar', n = 1350)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_vs_0_stat_no_fdr.jpeg', dpi = 300)


############# 4. прериск против 0 #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/preisk_vs_0', exist_ok = True)
folder_out = 'preisk_vs_0'
p1 = 'prerisk'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, 'comb_planar', n = 1350)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/prerisk_vs_0_stat_no_fdr.jpeg', dpi = 300)


############# 5. нериск против 0 #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/norisk_vs_0', exist_ok = True)
folder_out = 'norisk_vs_0'
p1 = 'norisk'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, 'comb_planar', n = 1350)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1),  treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/norisk_vs_0_stat_no_fdr.jpeg', dpi = 300)



# Какая то ерунда, на TF plots просто серый фон - надо разбираться
'''
############# 6. позитивный фидбэк против негативного в рисках #########################################
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_40_comb_planars/comb_planars_fb_separ'

os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/risk_pos_vs_neg', exist_ok = True)
folder_out = 'risk_pos_vs_neg'

p1 = 'risk_fb_cur_positive'
p2 = 'risk_fb_cur_negative'

_, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, 'comb_planar', n = 1350)

fig = plot_deff_topo(p_val, donor, mean1, mean2, folder_out, title = "Average channel {0} vs {1}".format(p2, p1), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_pos_vs_neg_stat_no_fdr.jpeg', dpi = 300)


############# 7. позитивный фидбэк против 0 в рисках #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/risk_pos_vs_0', exist_ok = True)
folder_out = 'risk_pos_vs_0'
p1 = 'risk_fb_cur_positive'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, 'comb_planar', n = 1350)

fig = plot_topo_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1),  treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_fb_positive_vs_0_stat_no_fdr.jpeg', dpi = 300)

############# 8. позитивных фидбэк против 0 в рисках #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/risk_neg_vs_0', exist_ok = True)
folder_out = 'risk_neg_vs_0'
p1 = 'risk_fb_cur_negative'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, 'comb_planar', n = 1350)

fig = plot_topo_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_fb_negative_vs_0_stat_no_fdr.jpeg', dpi = 300)
'''
