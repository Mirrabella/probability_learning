#Ttest for sources
# Based on Script of Nikita Tyulenev: source_plot_get_full_stc.py
# Look Ttest_for_sources.ipynb for explanations

import os
import mne
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats import multitest as mul
from functions import signed_p_val


# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

vect_signed_p_val = np.vectorize(signed_p_val)

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

#freq_range = 'beta_16_30'

subjects = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/sources/subj_list.csv')['subj_list'].tolist()

subjects.remove('P062') #without MRI
subjects.remove('P052') # bad segmentation, попробовали запустить freesurfer еще раз не помогло

subjects.remove('P032') #ValueError: dimension mismatch - попробовали запустить freesurfer еще раз не помогло. Надо разбираться

subjects.remove('P045') #RuntimeError: Could not find neighbor for vertex 4395 / 10242 когда использую для задания пространства источников src, ico5 вместо oct6

inter = [-0.800, 2.400] # time interval


# download donor stc
stc_test = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/beta_16_30_stc_fsaverage_ave_into_subj/P001_risk_fb_cur_negative', 'fsaverage').crop(tmin=inter[0], tmax=inter[1], include_tmax=True)


# make folder for output files
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_pos_vs_neg' , exist_ok = True)

data_dir = '/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/beta_16_30_stc_fsaverage_ave_into_subj'
#################### Ttest between feedback inside the condition ###############################

for t in trial_type:
    comp1_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
    comp2_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
    for ind, subj in enumerate(subjects):
        #print(ind + 1, subj)
        temp1 = mne.read_source_estimate(os.path.join(data_dir, "{0}_{1}_fb_cur_{2}-lh.stc".format(subj, t, feedback[0]))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
        #temp1.resample(40)
        comp1_per_sub[ind, :, :] = temp1.data
        temp2 = mne.read_source_estimate(os.path.join(data_dir, "{0}_{1}_fb_cur_{2}-lh.stc".format(subj, t, feedback[1]))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
        #temp2.resample(40)
        comp2_per_sub[ind, :, :] = temp2.data
        
    print(comp1_per_sub.shape)
    print(comp2_per_sub.shape)

    t_stat, p_val = stats.ttest_rel(comp2_per_sub, comp1_per_sub, axis=0)
    
    print(p_val.min(), p_val.mean(), p_val.max())
    print(t_stat.min(), t_stat.mean(), t_stat.max())
    
    # full FDR
    
    width, height = p_val.shape
    p_val_resh = p_val.reshape(width * height)
    _, p_val = mul.fdrcorrection(p_val_resh)
    p_val = p_val.reshape((width, height))
    
    
    p_val = vect_signed_p_val(t_stat, p_val)
    
    # save the p value plotting on the brain (fsaverage)
    
    stc_test.data = p_val
    stc_test.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_pos_vs_neg/{0}_fb_cur_pos_vs_neg_pval_full_fdr'.format(t))
    
    # save the beta difference plotting on the brain (fsaverage)
    
    
    mean_data = (comp2_per_sub - comp1_per_sub).mean(axis=0) # усредняем между испытуемыми
    stc_test.data = mean_data
    stc_test.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_pos_vs_neg/{0}_fb_cur_pos_vs_neg_mean_beta'.format(t))
    

#################### Ttest between the conditions ###############################    

trial_type = ['prerisk', 'risk', 'postrisk']

# change data dir
data_dir = '/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/beta_16_30_stc_fsaverage_ave_into_subj_united_fb'
# make folder for output files
os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_between_choice_type' , exist_ok = True)

    
for t in trial_type:
    comp1_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
    comp2_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
    for ind, subj in enumerate(subjects):
        #print(ind + 1, subj)
        temp1 = mne.read_source_estimate(os.path.join(data_dir, "{0}_norisk-lh.stc".format(subj))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
        #temp1.resample(40)
        comp1_per_sub[ind, :, :] = temp1.data
        temp2 = mne.read_source_estimate(os.path.join(data_dir, "{0}_{1}-lh.stc".format(subj, t))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
        #temp2.resample(40)
        comp2_per_sub[ind, :, :] = temp2.data
        
    print(comp1_per_sub.shape)
    print(comp2_per_sub.shape)

    t_stat, p_val = stats.ttest_rel(comp2_per_sub, comp1_per_sub, axis=0)
    
    print(p_val.min(), p_val.mean(), p_val.max())
    print(t_stat.min(), t_stat.mean(), t_stat.max())
    
    # full FDR
    
    width, height = p_val.shape
    p_val_resh = p_val.reshape(width * height)
    _, p_val = mul.fdrcorrection(p_val_resh)
    p_val = p_val.reshape((width, height))
    
    
    p_val = vect_signed_p_val(t_stat, p_val)
    
    # save the p value plotting on the brain (fsaverage)
    
    stc_test.data = p_val
    stc_test.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_between_choice_type/norisk_vs_{0}_pval_full_fdr'.format(t))
    
    # save the beta difference plotting on the brain (fsaverage)
    
    
    mean_data = (comp2_per_sub - comp1_per_sub).mean(axis=0) # усредняем между испытуемыми
    stc_test.data = mean_data
    stc_test.save('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/ttest_between_choice_type/norisk_vs_{0}_mean_beta'.format(t))    







