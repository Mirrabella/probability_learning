

import os
import os.path as op
import mne
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats import multitest as mul


# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
#subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'
mne.viz.set_3d_options(antialias=False)

#read label 
label_rh = mne.read_label('/net/server/data/Archive/prob_learn/freesurfer/fsaverage/label/rh.Medial_wall.label', 'fsaverage' )
label_lh = mne.read_label('/net/server/data/Archive/prob_learn/freesurfer/fsaverage/label/lh.Medial_wall.label', 'fsaverage' )

scale_pvalue = [0.95, 0.99, 1.0]
scale = [[0.15, 0.27, 0.84], [0.15, 0.27, 0.84], [0.48, 0.70, 0.85]]


data_path = '/net/server/data/Archive/prob_learn/pultsinak/sources_sLoreta/averege_betwen_subj'

intervals = ['lp_hp_900_300', 'lp_hp_1100_1500', 'pos_neg_1500_1900']
pval = [
    ['risk_vs_norisk_pval_nofdr_900_300', 
    'risk_vs_norisk_pval_full_fdr_900_300'], 
    ['after_fb_lp_vs_hp_pval_nofdr_1100_1400', 
    'after_fb_lp_vs_hp_pval_fullfdr_1100_1400'], 
    ['after_fb_lp_pos_vs_neg_pval_nofdr_1500_1900-lh.stc', 
    'after_fb_lp_pos_vs_neg_pval_fullfdr_1500_1900-lh.stc']
] 

mean_beta = ['risk_vs_norisk_mean_beta_900_300', 'after_fb_lp_vs_hp_pval_mean_beta_1100_1400', 'after_fb_lp_pos_vs_neg_mean_beta_1500_1900']

scale_pvalue = [0.95, 0.99, 1.0]   

for i, inter in enumerate(intervals):

    stc_pvalue_nofdr = mne.read_source_estimate(op.join(data_path, '{0}/{1}'.format(inter, pval[i][0])), 'fsaverage')
    stc_pvalue_fdr = mne.read_source_estimate(op.join(data_path, '{0}/{1}'.format(inter, pval[i][1])), 'fsaverage')
    
    stc_pval = [stc_pvalue_nofdr, stc_pvalue_fdr]
    stc_pval_name = ['stc_pvalue_nofdr', 'stc_pvalue_fdr']
    # plotting pval
    ###########################
    for s, sp in enumerate(stc_pval):
        brain = mne.viz.plot_source_estimates(sp, hemi='split', time_viewer=False, background='white', 
                                                  foreground = 'black', cortex='bone', size = (1200, 600),
                                                        views = ['lat', 'med'], clim = dict(kind = 'value', pos_lims = scale_pvalue), 
                                                  time_label=f'{inter}', spacing ='ico5', title = f'{stc_pval_name[s]} , {inter}')
          
                                                       
        brain.add_text(0.0, 0.9, f'{stc_pval_name[s]}, {inter}, **{scale_pvalue}**',
                               font_size=12, color='black')


        brain.save_image('/home/vtretyakova/Рабочий стол/probability_learning/sources/Visualization/plot_source_contrasts/{0}_{1}.png'.format(stc_pval_name[s], inter))
        brain.close()
    ############################
    
    # Nullify insignificants vertices
    #################################
    stc_pvalue_lh_reshape = np.reshape(stc_pvalue_nofdr.lh_data, 10242)
    stc_pvalue_rh_reshape = np.reshape(stc_pvalue_nofdr.rh_data, 10242)

    index_lh = []

    for ind, p in enumerate(stc_pvalue_lh_reshape):
        if p >= 0.95 or p <= -0.95:
            index_lh.append(ind)
            
    index_rh = []

    for ind, p in enumerate(stc_pvalue_rh_reshape):
        if p >= 0.95 or p <= -0.95:
            index_rh.append(ind)
            
            
    stc_data = mne.read_source_estimate(op.join(data_path, '{0}/{1}'.format(inter, mean_beta[i])), 'fsaverage')
            
    stc_data_lh_reshape = np.reshape(stc_data.lh_data, 10242)
    stc_data_rh_reshape = np.reshape(stc_data.rh_data, 10242)
    
    # both hemi
    hemisphere = [0,1]
    indexes = [index_lh, index_rh]
    stc_reshape_hemi = [stc_data_lh_reshape, stc_data_rh_reshape]
    for idx in hemisphere:
        for j in stc_data.vertices[idx]:
            if j not in indexes[idx]:
                stc_reshape_hemi[idx][j] = 0
        
    ###################################
    
    # dropping Median Wall
    #############################

# hemi separate
    stc_in_label_lh = stc_data.in_label(label_lh) 
    stc_in_label_rh = stc_data.in_label(label_rh) 
            
    list_of_index_lh = stc_in_label_lh.vertices[0].tolist()
    list_of_index_rh = stc_in_label_rh.vertices[1].tolist()
    
# both hemi
    hemisphere = [0,1]
    indexes = [list_of_index_lh, list_of_index_rh]
    stc_reshape_hemi = [stc_data_lh_reshape, stc_data_rh_reshape]
    for h in hemisphere:
        for j in stc_data.vertices[h]:
            if j in indexes[h]:
                stc_reshape_hemi[h][j] = 0
                        
    stc_lh_new = stc_data_lh_reshape.reshape((10242, 1))
    stc_rh_new = stc_data_rh_reshape.reshape((10242, 1))
            
    stc_data.data[:10242] = stc_lh_new
    stc_data.data[10242:] = stc_rh_new 
    
    stc_data.save('/home/vtretyakova/Рабочий стол/probability_learning/sources/Visualization/plot_source_contrasts/{0}_mean_beta_sign_nofdr'.format(inter))   

    
    
    brain = mne.viz.plot_source_estimates(stc_data, hemi='split', time_viewer=False, background='white', 
                                                  foreground = 'black', cortex='bone', size = (1200, 600),
                                                        views = ['lat', 'med'], clim = dict(kind = 'value', 
                                                                                            pos_lims = scale[i]),
                                                       spacing ='ico5', title = f'{inter}')
          
                                                       
    brain.add_text(0.0, 0.9, f'**{scale[i]}**, {inter}',
                               font_size=12, color='black')
            #brain.add_text(0.0, 0.8, f'{inter[0]} .... inter[1]s',
                               #font_size=10, color='green')                   
            #brain.add_text(0.0, 0.8, '{beta power change}', font_size=10, color='blue')

    brain.save_image('/home/vtretyakova/Рабочий стол/probability_learning/sources/Visualization/plot_source_contrasts/{0}.png'.format(inter))
    brain.close()
    





            
            
