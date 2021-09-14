
import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from functions import ttest_pair, ttest_vs_zero, plot_deff_tf, plot_tf_vs_zero

freq_range = '2_40_step_2_time_bandwidth_by_default_4_early_log'

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

########################## Combined planars ####################################

# донор (donor creation see make_donor_for_tfr_plot.ipynb)
donor = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/donor_planar1_evoked.h5'.format(freq_range), condition=None)[0]

n = donor.data.shape[2] # количество временных точек (берем у донора, если донор из тех же данных.
fr = donor.data.shape[1] # number of frequencies  (берем у донора, если донор из тех же данных.

os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar'.format(freq_range), exist_ok = True)
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels'.format(freq_range), exist_ok = True)


data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/{0}_comb_planars'.format(freq_range)
############# 1. риск против нериска #########################################
'''
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/norisk_vs_risk'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/norisk_vs_risk'.format(freq_range)

p1 = 'norisk'
p2 = 'risk'


_, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, freq_range, 'comb_planar', fr, n)

fig = plot_deff_tf(p_val, donor, mean1, mean2, folder_out, title = "Average channel {0} vs {1}".format(p1, p2), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/risk_vs_norisk_no_fdr.jpeg'.format(freq_range), dpi = 300)

############# 2. прериск против нериска #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/norisk_vs_prerisk'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/norisk_vs_prerisk'.format(freq_range)


p1 = 'norisk'
p2 = 'prerisk'

_, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, freq_range, 'comb_planar', fr, n)

fig = plot_deff_tf(p_val, donor, mean1, mean2, folder_out, title = "Average channel {0} vs {1}".format(p1, p2), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/prerisk_vs_norisk_no_fdr.jpeg'.format(freq_range), dpi = 300)

############# 3. риск против 0 #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/risk_vs_0'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/risk_vs_0'.format(freq_range)

p1 = 'risk'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, freq_range, 'comb_planar', fr, n)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/risk_vs_0_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)


############# 4. прериск против 0 #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/preisk_vs_0'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/preisk_vs_0'.format(freq_range)
p1 = 'prerisk'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, freq_range, 'comb_planar', fr, n)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/prerisk_vs_0_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)


############# 5. нериск против 0 #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/norisk_vs_0'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/norisk_vs_0'.format(freq_range)
p1 = 'norisk'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, freq_range, 'comb_planar', fr, n)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1),  treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/norisk_vs_0_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)

'''
############# 6. позитивный фидбэк против негативного в рисках #########################################
#data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_20_tb_2_comb_planars/comb_planars_fb_separ'

os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/risk_pos_vs_neg'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/risk_pos_vs_neg'.format(freq_range)

p1 = 'risk_fb_cur_positive'
p2 = 'risk_fb_cur_negative'

_, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, freq_range, 'comb_planar', fr, n)

fig = plot_deff_tf(p_val, donor, mean1, mean2, folder_out, title = "Average channel {0} vs {1}".format(p1, p2), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/risk_pos_vs_neg_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)


############# 7. позитивный фидбэк против 0 в рисках #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/risk_pos_vs_0'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/risk_pos_vs_0'.format(freq_range)
p1 = 'risk_fb_cur_positive'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, freq_range, 'comb_planar', fr, n)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1),  treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/risk_fb_positive_vs_0_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)

############# 8. позитивных фидбэк против 0 в рисках #########################################
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/risk_neg_vs_0'.format(freq_range), exist_ok = True)
folder_out = '{0}_comb_planar/risk_neg_vs_0'.format(freq_range)
p1 = 'risk_fb_cur_negative'

_, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, freq_range, 'comb_planar', fr, n)

fig = plot_tf_vs_zero(p_val, donor, mean1, folder_out, title = "Average channel {0} vs 0".format(p1), treshold = 0.05)
fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}/tfr_average_channels/risk_fb_negative_vs_0_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)
'''
############################ Отдельные планары ####################################

# донор (donor creation see make_donor_for_tfr_plot.ipynb)
donor_planar1 = mne.time_frequency.read_tfrs('/home/vtretyakova/Рабочий стол/time_frequency_plots/donor_2_20_1_evoked_planar1.h5', condition=None)[0]
donor_planar2 = mne.time_frequency.read_tfrs('/home/vtretyakova/Рабочий стол/time_frequency_plots/donor_2_20_1_evoked_planar2.h5', condition=None)[0]

os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels', exist_ok = True)
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/planar1_2_20', exist_ok = True)
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/planar2_2_20', exist_ok = True)

############# 1. риск против нериска #########################################
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_20_separ_planars/separ_planars_average_between_fb'

p1 = 'norisk'
p2 = 'risk'

planars = ['planar1', 'planar2']
donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/norisk_vs_risk'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/norisk_vs_risk'.format(planar)
    _, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, planar, n = 1350)

    fig = plot_deff_tf(p_val, donors[idx], mean1, mean2, folder_out, title = "Average channel {0} vs {1}, {2}".format(p1, p2, planar), treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/norisk_vs_risk_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)

############# 2. прериск против нериска #########################################
p1 = 'norisk'
p2 = 'prerisk'

planars = ['planar1', 'planar2']
donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/norisk_vs_prerisk'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/norisk_vs_prerisk'.format(planar)
    _, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, planar, n = 1350)

    fig = plot_deff_tf(p_val, donors[idx], mean1, mean2, folder_out, title = "Average channel {0} vs {1}, {2}".format(p1, p2, planar), treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/prerisk_vs_norisk_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)

############# 3. риск против 0 #########################################

p1 = 'risk'

planars = ['planar1', 'planar2']

donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/risk_vs_0'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/risk_vs_0'.format(planar)
    _, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, planar, n = 1350)

    fig = plot_tf_vs_zero(p_val, donors[idx], mean1, folder_out, title = "Average channel {0} vs 0, {1}".format(p1, planar), treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_vs_0_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)


############# 4. прериск против 0 #########################################

p1 = 'prerisk'

planars = ['planar1', 'planar2']
donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/preisk_vs_0'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/preisk_vs_0'.format(planar)
    _, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, planar, n = 1350)

    fig = plot_tf_vs_zero(p_val, donors[idx], mean1, folder_out, title = "Average channel {0} vs 0, {1}".format(p1, planar), treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/prerisk_vs_0_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)


############# 5. нериск против 0 #########################################
p1 = 'norisk'


planars = ['planar1', 'planar2']
donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/norisk_vs_0'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/norisk_vs_0'.format(planar)
    _, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, planar, n = 1350)

    fig = plot_tf_vs_zero(p_val, donors[idx], mean1, folder_out, title = "Average channel {0} vs 0, {1}".format(p1, planar),  treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/norisk_vs_0_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)


############# 6. позитивный фидбэк против негативного в рисках #########################################
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_20_separ_planars/separ_planars_separ_fb'

p1 = 'risk_fb_cur_positive'
p2 = 'risk_fb_cur_negative'

planars = ['planar1', 'planar2']
donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/risk_pos_vs_neg'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/risk_pos_vs_neg'.format(planar)

    _, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, planar, n = 1350)

    fig = plot_deff_tf(p_val, donors[idx], mean1, mean2, folder_out, title = "Average channel {0} vs {1}, {2}".format(p1, p2, planar), treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_pos_vs_neg_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)


############# 7. позитивный фидбэк против 0 в рисках #########################################
p1 = 'risk_fb_cur_positive'

planars = ['planar1', 'planar2']
donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/risk_pos_vs_0'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/risk_pos_vs_0'.format(planar)
    _, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, planar, n = 1350)

    fig = plot_tf_vs_zero(p_val, donors[idx], mean1, folder_out, title = "Average channel {0} vs 0, {1}".format(p1, planar),  treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_fb_positive_vs_0_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)

############# 8. позитивных фидбэк против 0 в рисках #########################################
p1 = 'risk_fb_cur_negative'

planars = ['planar1', 'planar2']
donors = [donor_planar1, donor_planar2]

for idx, planar in enumerate(planars):
    os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_2_20/risk_neg_vs_0'.format(planar), exist_ok = True)
    folder_out = '/{0}_2_20/risk_neg_vs_0'.format(planar)
    _, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, planar, n = 1350)

    fig = plot_tf_vs_zero(p_val, donors[idx], mean1, folder_out, title = "Average channel {0} vs 0, {1}".format(p1, planar), treshold = 0.05)
    fig.savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/tfr_average_channels/risk_fb_negative_vs_0_2_20_stat_no_fdr_{0}.jpeg'.format(planar), dpi = 300)
    
'''    
    
    
    

