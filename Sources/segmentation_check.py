# Head Model: BEM (boundary element model) surface - создается отдельно для каждого испытуемого

import os.path as op
import os
import mne


# This code sets an environment variable called SUBJECTS_DIR
#os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'



subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]


# удаляем испытуемых без МРТ        
subjects.remove('P036')
subjects.remove('P062')        


for subj in subjects:
        
    fig = mne.viz.plot_bem(subj, subjects_dir, brain_surfaces='white', orientation='coronal', show = False);
    
    fig.savefig('/home/vtretyakova/Рабочий стол/probability_learning/sources/segmentation_check/{0}.jpeg'.format(subj), dpi = 300)
    
    
    
    
    
    
