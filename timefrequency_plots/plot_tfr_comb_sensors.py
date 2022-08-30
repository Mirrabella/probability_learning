
import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from functions import ttest_pair, ttest_vs_zero, ttest_pair_comb_channels, ttest_vs_zero_comb_channels, plot_deff_tf_comb_channels, plot_tf_vs_zero_comb_channels, plot_deff_tf_comb_channels_without_stat, plot_tf_vs_zero_comb_channels_without_stat

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

#os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar'.format(freq_range), exist_ok = True)
os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta', exist_ok = True)


data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/{0}/{0}_comb_planars'.format(freq_range)
#os.makedirs('/home/vtretyakova/Рабочий стол/time_frequency_plots/{0}_comb_planar/norisk_vs_risk'.format(freq_range), exist_ok = True)
folder_out = 'article_beta'

############# 1. Differents #########################################
'''
# choice type differents
p1 = 'norisk'
p2 = 'risk'

# diff between fb inside choice types
#p1 = 'risk_fb_cur_positive'
#p2 = 'risk_fb_cur_negative'


best_chan_list = [68, 75, 76]
interval = 'decision_making'

#best_chan_list = [76, 77, 70]
#interval = 'early_fb'

#best_chan_list = [10, 12, 20]
#interval = 'late_fb_anterior'

#best_chan_list = [60, 69, 76]
#interval = 'late_fb_posterior'

_, p_val, mean1, mean2 = ttest_pair_comb_channels(data_path, subjects, p1, p2, freq_range, 'comb_planar', fr, n, best_chan_list)

b, b_stat = plot_deff_tf_comb_channels(p_val, donor, mean1, mean2, folder_out, treshold = 0.05)


b[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/{0}_norisk_vs_risk_chan_{1}_{2}_{3}_scale_2_0.png'.format(interval, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)
b_stat[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/{0}_norisk_vs_risk_chan_{1}_{2}_{3}_no_fdr_scale_2_0.png'.format(interval, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)

#b[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/{0}_risk_pos_vs_neg_chan_{1}_{2}_{3}_scale_2_0.png'.format(interval, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)
#b_stat[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/{0}_risk_pos_vs_neg_chan_{1}_{2}_{3}_no_fdr_scale_2_0.png'.format(interval, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)

'''

############# 2. Choice types против 0 #########################################

#best_chan_list = [68, 75, 76]
#interval = 'decision_making'

#best_chan_list = [76, 77, 70]
#interval = 'early_fb'

#best_chan_list = [10, 12, 20]
#interval = 'late_fb_anterior'

best_chan_list = [60, 69, 76]
interval = 'late_fb_posterior'


#p1s = ['risk', 'norisk']
p1s = ['risk_fb_cur_positive', 'risk_fb_cur_negative']

for p1 in p1s:

    _, p_val, mean1 = ttest_vs_zero_comb_channels(data_path, subjects, p1, freq_range, 'comb_planar', fr, n, best_chan_list)

    b, b_stat = plot_tf_vs_zero_comb_channels(p_val, donor, mean1, folder_out, treshold = 0.05)

    b[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/{0}_0_vs_{1}_chan_{2}_{3}_{4}.png'.format(interval, p1, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)
    b_stat[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/{0}_0_vs_{1}_chan_{2}_{3}_{4}_no_fdr.png'.format(interval, p1, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)


############# 4. Differents without statistics #########################################
'''
# choice type differents
p1 = 'norisk'
p2 = 'risk'

# diff between fb inside choice types
#p1 = 'risk_fb_cur_positive'
#p2 = 'risk_fb_cur_negative'


best_chan_list = [68, 75, 76]
interval = 'decision_making'

#best_chan_list = [76, 77, 70]
#interval = 'early_fb'

#best_chan_list = [10, 12, 20]
#interval = 'late_fb_anterior'

#best_chan_list = [60, 69, 76]
#interval = 'late_fb_posterior'

_, p_val, mean1, mean2 = ttest_pair(data_path, subjects, p1, p2, freq_range, 'comb_planar', fr, n)

b = plot_deff_tf_comb_channels_without_stat(p_val, donor, mean1, mean2, folder_out, best_chan_list)
'''

#b[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/without_stat/{0}_norisk_vs_risk_chan_{1}_{2}_{3}_without_stat.png'.format(interval, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)

b[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/without_stat/{0}_risk_pos_vs_neg_chan_{1}_{2}_{3}_without_stat_scale_2_0.png'.format(interval, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)

############# 4. Choice types против 0, without stat #########################################
'''
best_chan_list = [68, 75, 76]
interval = 'decision_making'

#best_chan_list = [76, 77, 70]
#interval = 'early_fb'

#best_chan_list = [10, 12, 20]
#interval = 'late_fb_anterior'

#best_chan_list = [60, 69, 76]
#interval = 'late_fb_posterior'


p1s = ['risk', 'norisk']
#p1s = ['risk_fb_cur_positive', 'risk_fb_cur_negative']

for p1 in p1s:

    _, p_val, mean1 = ttest_vs_zero(data_path, subjects, p1, freq_range, 'comb_planar', fr, n)

    b = plot_tf_vs_zero_comb_channels_without_stat(p_val, donor, mean1, folder_out, best_chan_list)

    b[0].savefig('/home/vtretyakova/Рабочий стол/time_frequency_plots/article_beta/without_stat/{0}_0_vs_{1}_chan_{2}_{3}_{4}_without_stat.png'.format(interval, p1, best_chan_list[0], best_chan_list[1], best_chan_list[2]), dpi = 300)
'''    

    
    
    
    

