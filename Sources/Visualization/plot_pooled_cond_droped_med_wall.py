

import os
import mne
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats import multitest as mul


# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
#subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/pool_cond', exist_ok = True)
#os.makedirs('/net/server/data/Archive/prob_learn/vtretyakova/sources/beta_16_30/plot_sources_mean_beta' , exist_ok = True)
mne.viz.set_3d_options(antialias=False)
'''
intervals = [[1.100, 1.500]] # time intervals for averaging
name_int =['early_after_fb']
mean_time = [1.3]

#scale (0.15, 0.27, 0.84)
'''
intervals = [[-0.900, -0.300]] # time intervals for averaging
name_int =['before_resp']
mean_time = [-0.6]
# scale (0.15, 0.25, 1.14)

'''
intervals = [[1.500, 1.900]] # time intervals for averaging
name_int =['late_after_fb']
mean_time = [1.7]
'''
# scale 0.17, 0.39, 1.14

#read label 
label_rh = mne.read_label('/net/server/data/Archive/prob_learn/freesurfer/fsaverage/label/rh.Medial_wall.label', 'fsaverage' )
label_lh = mne.read_label('/net/server/data/Archive/prob_learn/freesurfer/fsaverage/label/lh.Medial_wall.label', 'fsaverage' )




for idx, inter in enumerate(intervals):


    #for cond in trial_type:
        #for ind, v in enumerate(var_of_ploting):
            stc_pooled_ch_t = mne.read_source_estimate('/net/server/data/Archive/prob_learn/pultsinak/sources_sLoreta/pooled_choice/all_ChT', 'fsaverage')
            stc_pooled_ch_t_int = stc_pooled_ch_t.copy().crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
            stc_pooled_ch_t_int = stc_pooled_ch_t_int.mean() # average between time points
            
            # hemi separate
            stc_in_label_lh = stc_pooled_ch_t_int.in_label(label_lh) 
            stc_in_label_rh = stc_pooled_ch_t_int.in_label(label_rh) 
            
            list_of_index_lh = stc_in_label_lh.vertices[0].tolist()
            list_of_index_rh = stc_in_label_rh.vertices[1].tolist()
            
            stc_lh_reshape = np.reshape(stc_pooled_ch_t_int.lh_data, 10242) # left hemi
            stc_rh_reshape = np.reshape(stc_pooled_ch_t_int.rh_data, 10242) # right hemi
            
            # both hemi
            hemisphere = [0,1]
            indexes = [list_of_index_lh, list_of_index_rh]
            stc_reshape_hemi = [stc_lh_reshape, stc_rh_reshape]
            for i in hemisphere:
                for j in stc_pooled_ch_t_int.vertices[i]:
                    if j in indexes[i]:
                        stc_reshape_hemi[i][j] = 0
                        
            stc_lh_new = stc_lh_reshape.reshape((10242, 1))
            stc_rh_new = stc_rh_reshape.reshape((10242, 1))
            
            stc_pooled_ch_t_int.data[:10242] = stc_lh_new
            stc_pooled_ch_t_int.data[10242:] = stc_rh_new
            
                        
            scale = [0.15, 0.25, 1.14]
            #scale = [0.17, 0.39, 1.14]
            #for t in time_points:
            brain = mne.viz.plot_source_estimates(stc_pooled_ch_t_int, hemi='split', time_viewer=False, background='white', 
                                                  foreground = 'black', cortex='bone', size = (1200, 600),
                                                        views = ['lat', 'med'], clim = dict(kind = 'value', 
                                                                                            pos_lims = scale),
                                                  time_label=f'{inter[0]} .... {inter[1]} s',
                                                       spacing ='ico5', title = f'pooled choice types, beta power 16 - 30 Hz, {inter[0]} .... {inter[1]} s')
          
                                                       
            brain.add_text(0.0, 0.9, f'pooled choice types, beta 16-30Hz, **{scale}**, {inter[0]} .... inter[1]s',
                               font_size=12, color='black')
            #brain.add_text(0.0, 0.8, f'{inter[0]} .... inter[1]s',
                               #font_size=10, color='green')                   
            #brain.add_text(0.0, 0.8, '{beta power change}', font_size=10, color='blue')

            brain.save_image('/home/vtretyakova/Рабочий стол/probability_learning/sources/Visualization/plot_source/{0}_all_choice_types_1.jpeg'.format(name_int[idx]))
            brain.close()
        

            
            
