
import os


###################### переименовываем файлы в папке, чтобы можно было воспользоваться функциями ####################
os.chdir('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/tfr_plots/h5_2_40_comb_planars/comb_planars_fb_separ')
subjects_for_rename = []
for i in range(0,63):
    if i < 10:
        subjects_for_rename += ['P00' + str(i)]
    else:
        subjects_for_rename += ['P0' + str(i)]
    
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['fb_cur_positive', 'fb_cur_negative']

for s in subjects_for_rename:
    for t in trial_type:
        for fb in feedback:
            try:
                os.rename("{0}_{1}_average_2_40_resp_comb_planar_{2}.h5".format(s, t, fb), "{0}_{1}_{2}_average_2_40_resp_comb_planar.h5".format(s, t, fb))
            
            except (OSError):
                print('This file not exist')
            

