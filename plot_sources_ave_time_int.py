

import os
import mne
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats import multitest as mul


# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
#subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

scale_pvalue = [0.95, 0.99, 1.0]
#scale_mean_beta_between_fb = [0.43, 0.63, 1.3]
scale_mean_beta_between_fb = [0.15, 0.27, 0.84] # for norisk pos vs neg (value of differents is smaller (see topomaps))
#scale_mean_beta_between_choice_types = [0.1, 0.35, 1.2]
scale_mean_beta_between_choice_types = [0.01, 0.25, 1.01] # for norisk vs postrisk (value of differents is smaller (see topomaps))
var_of_ploting = ['pval_nofdr', 'pval_full_fdr', 'mean_beta']
#var_of_ploting = ['pval_full_fdr']

resample = 'Усредняем бету на временном интервале с помощью mean()'


'''
# donor for time points
donor = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_pos_vs_neg_100_ms/risk_fb_cur_pos_vs_neg_pval_nofdr', 'fsaverage')

a = donor.times.tolist()

time_points = []
for i in a:
    c = round(float(i), 1)
    time_points.append(c)
'''    
    
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/plot_sources_ttest_in_ave_int', exist_ok = True)
#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/plot_sources_mean_beta' , exist_ok = True)

intervals = [[-0.900, -0.100], [0.700, 0.900], [1.500, 1.900]] # time intervals for averaging
name_int =['before_resp', 'before_fb', 'after_fb']
mean_time = [-0.5, 0.8, 1.7]

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################
# for p_value
lines = ["resample: {}".format(resample), "intervals: {}".format(intervals), "name_int: {}".format(name_int), "scale_pvalue: {}".format(scale_pvalue), "scale_mean_beta_between_fb : {}".format(scale_mean_beta_between_fb), "scale_mean_beta_between_choice_types : {}".format(scale_mean_beta_between_choice_types)]


with open("/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/plot_sources_ttest/config.txt", "w") as file:
    for  line in lines:
        file.write(line + '\n')



################ contrast for feedbacks inside choice (trial) types #################
'''
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk']

scale = [scale_pvalue, scale_pvalue, scale_mean_beta_between_fb]
#scale = [scale_pvalue]

for idx, inter in enumerate(intervals):


    for cond in trial_type:
        for ind, v in enumerate(var_of_ploting):
            stc_pos_vs_neg = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_on_ave_int/{0}_fb_cur_pos_vs_neg_{1}_{2}'.format(cond, v, name_int[idx]), 'fsaverage')
        
            #for t in time_points:
            brain = mne.viz.plot_source_estimates(stc_pos_vs_neg, hemi='split', time_viewer=False, background='white', 
                                                  foreground = 'black', cortex='bone', size = (1200, 600),
                                                        views = ['lat', 'med'], clim = dict(kind = 'value', 
                                                                                            pos_lims = scale[ind]), 
                                                  initial_time = mean_time[idx], time_label=f'{inter[0]} .... {inter[1]} s',
                                                       spacing ='ico5', title = f'{cond} neg vs pos, beta power 16 - 30 Hz, {inter[0]} .... {inter[1]} s')
          
                                                       
            brain.add_text(0.0, 0.9, f'{cond} pos vs neg, beta 16-30Hz, **{scale[ind]}**',
                               font_size=12, color='black')
            #brain.add_text(0.0, 0.8, f'{inter[0]} .... inter[1]s',
            #                   font_size=10, color='green')                   
            brain.add_text(0.0, 0.8, f'{v}', font_size=10, color='blue')

            brain.save_image('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/plot_sources_ttest_in_ave_int/{0}_{1}_neg_vs_pos_{2}.jpeg'.format(name_int[idx], cond, v))
            brain.close()
        
''' 
################ contrast for choice (trial) types #################

trial_type = ['prerisk', 'risk', 'postrisk']
#trial_type = ['postrisk']

scale = [scale_pvalue, scale_pvalue, scale_mean_beta_between_choice_types]
#scale = [scale_pvalue]

for idx, inter in enumerate(intervals):
    for cond in trial_type:
        for ind, v in enumerate(var_of_ploting):
            stc = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_on_ave_int/norisk_vs_{0}_{1}_{2}'.format(cond, v, name_int[idx]), 'fsaverage')
    
        
            brain = mne.viz.plot_source_estimates(stc, hemi='split', time_viewer=False, background='white', 
                                                  foreground = 'black', cortex='bone', size = (1200, 600),
                                                        views = ['lat', 'med'], clim = dict(kind = 'value', 
                                                                                            pos_lims = scale[ind]), 
                                                  initial_time = mean_time[idx], time_label=f'{inter[0]} .... {inter[1]} s',
                                                       spacing ='ico5', title = f'norisk vs {cond}, beta power 16 - 30 Hz, {inter[0]} .... {inter[1]} s')
          
                                                       
            brain.add_text(0.0, 0.9, f'norisk vs {cond}, beta 16-30Hz, **{scale[ind]}**',
                               font_size=12, color='black')
                               
            #brain.add_text(0.0, 0.8, f'{inter[0]} .... inter[1]s',
            #                       font_size=10, color='green')  
            brain.add_text(0.0, 0.8, f'{v}', font_size=10, color='blue')

            brain.save_image('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/plot_sources_ttest_in_ave_int/{0}_norisk_vs_{1}_{2}.jpeg'.format(name_int[idx], cond, v))
            brain.close()
                
            
            
            
            
