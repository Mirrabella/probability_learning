### For more details see plot_timecourses Jupyter Notebook  ######

import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
import copy
import pandas as pd
from scipy import stats
from function import combine_planar_Evoked, plot_topo_vs_zero


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

# donor
donor = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_2_steps/P001_norisk_evoked_beta_16_30_resp.fif')

time_len = len(donor.times) # количество временных отчетов


n = 0 # считаем количество испытуемых
data_for_mean = np.empty((0, 102, time_len)) # задаем массив, куда будем складывать данные для каждого испытуемого и затем усредним
for subj in subjects:
    try:
        evoked = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_2_steps/{0}_norisk_evoked_beta_16_30_resp.fif'.format(subj))
        _, _, combined = combine_planar_Evoked(evoked)
        combined_for_subject = combined.reshape(1, 102, time_len)
        data_for_mean = np.vstack([data_for_mean, combined_for_subject])
        n = n+1
    except (OSError):
        print('This file not exist')
    
mean_subj = data_for_mean.mean(axis = 0) # усредняем между испытуемыми
    
grand_average = mean_subj.mean(axis = 0) #усредняем между сенсорами

##################### timecourse ###############################
plt.figure() #создаем рисунок 
plt.rcParams['axes.facecolor'] = 'none' # делаем его прозрачным
plt.xlim(-1.5, 2.5) #назначаем границы рисунка по х
plt.ylim(-3.0, 0.5) #назначаем границы рисунка по у
plt.title('norisk', fontsize = 8) 
plt.plot([0, 0.001], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1) # вертикальная линия, которая показывает, где находится наше событие
plt.plot([-6, 6], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1) # нулевая линия по горизонтали

plt.plot(donor.times, grand_average, color='b', linewidth=3) # рисует график первого кондишена (всегда синий)
    
# сохраняем в формате .jpeg
plt.savefig('/home/vtretyakova/Рабочий стол/probability_learning/timecourses/norisk_{0}.jpeg'.format(n), transparent=True)
plt.close()  

######################## topomap #######################
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

#n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

t_stat, p_val = stats.ttest_1samp(data_for_mean, 0, axis=0)
norisk_mean = data_for_mean.mean(axis=0)
fig, temp = plot_topo_vs_zero(p_val, temp, norisk_mean, time_to_plot, title = 'norisk vs zero, no FDR,  {0} subjects'.format(n))

fig.savefig('/home/vtretyakova/Рабочий стол/probability_learning/timecourses/risk_vs_0_stat_no_fdr.jpeg', dpi = 300)




'''
def plot_time_course_grand_average(grand_avarage_data, time, title = 'figure', xmin = -1.5, xmax = 2.5,
                                   ymin = -2.1, ymax = 0.5, color='b', outpath):
    
    
    plt.figure() #создаем рисунок 
    plt.rcParams['axes.facecolor'] = 'none' # делаем его прозрачным
    plt.xlim(xmin, xmax) #назначаем границы рисунка по х
    plt.ylim(ymin, ymax) #назначаем границы рисунка по у
    plt.title(title, fontsize = 8) 
    plt.plot([0, 0.001], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1) # вертикальная линия, которая показывает, где находится наше событие
    plt.plot([-6, 6], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1) # нулевая линия по горизонтали

    plt.plot(time, grand_avarage_data, color=color, linewidth=3) # рисует график первого кондишена (всегда синий)
    
    # сохраняем в формате .jpeg
    plt.savefig('{0}/{1}.jpeg'.format(outpath, title), transparent=True)
    plt.close()  

'''





