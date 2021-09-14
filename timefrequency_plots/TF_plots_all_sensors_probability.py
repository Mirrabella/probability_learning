
###################### TF plots averange on every sensors (just as they are on the head) ############################

import mne
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import os.path as op
import pdfkit
import statsmodels.stats.multitest as mul
import re

from functions import clear_html, add_str_html, to_str_ar, add_pic_html


####################### Задаем необходимые параметры ############################

# Создаем или указываем папку куда будем сохранять рисунки
output = '/home/vera/MNE/time_frequency_plots/2_40_step_2_time_bandwidth_by_default_4_early_log_comb_planar/all_sensors'
rewrite = True
os.makedirs(output, exist_ok=True)

############### !!!!!!!!!!!!!! проверить информацию ################# 
# задаем планар (ненужное закомментировать) #0
#p = 'planar1'
#p = 'planar2'
p = 'comb_planar'
 

# Координаты сенсоров лежат в файле MatLab, мы их вынимаем и берем только последние 102 значения для комбайнов, и первые 204 для отдельных планаров (ненужное закомментировать)
# которые соответствуют комбайн планарам, первые 204 - это отвдельные планары
pos = io.loadmat('/home/vera/MNE/Paint_Nikita/pos_store.mat')['pos']

# Для отдельных планаров (если строим на листе сразу оба)
#pos = pos[:204] #первые 204 - это отдельные планары

#Для комбайн планаров  и если строим только один планар
pos = pos[204:] # берем только последние 102, первые 204 - это отдельные планары
pos.shape

# Тоже самое и с названиями каналов (ненужное закомментировать)
chan_labels_full = to_str_ar(io.loadmat('/home/vera/MNE/Paint_Nikita/channel_labels.mat')['chanlabels'])

# Для отдельных планаров
'''
chan_labels_planars = chan_labels_full[:204]
chan_labels = []
for i in chan_labels_planars:
    # разделяем строку по букве G (как в MEG0632.jpeg)
    b = re.split('G+', i)
    # получаем список из двух элементов берем 2ой, там где цифры и разделяем по точке, чтобы разделить разширение
    c = b[1].split(".")
    # берем первый элемент, где только цифры и делаем из них список, а затем делаем их числами (int())
    result = list(c[0])
    integer = []
    for k in result:
        integer.append(int(k))
        
    if p == 'planar1' and integer[3] == 2:
        chan_labels.append(i)
                
    elif p == 'planar2' and integer[3] == 3:
        chan_labels.append(i)
'''

#Для комбайн планаров
chan_labels = chan_labels_full[204:] # берем только последние 102, первые 204 - это отдельные планары

# настройки pdf документа
# Эта строка необходима дла Windows
#config = pdfkit.configuration(wkhtmltopdf='D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

options = {
    'orientation': 'landscape',
    'margin-bottom': '0in',
    'margin-left': '0in',
    'margin-right': '0in',
    'margin-top': '0in',
    'page-size': 'a3',
    'page-height': '18.33in',
    'page-width': '14in'
}

# словарь, где хранятся более полные названия
diction = {"stim": "from stimulus ",
           "react": "from reaction ",
           "fb_cur": "from current feedback",
           "all": "from stimulus (all)",
           "st": "start",
           "end": "end"
           }

################################# !!!!!!!!!!!!!!!!!!!!!!!!!!!! проверяем информацию в 3 местах по коду ниже  ##############################
# С каким названием сохраниться рисунок. Список имел смысл, когда строили и отдельные планары и комбайны.
# сейчас в этом нет необходимости, но возможно придется вернуться и отдельным

############################### Если по одному рисунку ###################################
'''
planars = ['0_vs_risk_pos_comb_planar_ttest_no_fdr'] #1

#папка откуда берем картинки
pic_folder = '/home/vera/MNE/time_frequency_plots/comb_planar/risk_pos_vs_0' #2

for ind, planar in enumerate(planars):
    #задаем имя нашей страницы
    html_name = "/home/vera/MNE/Paint_Nikita/topomaps_pdf/my.html"
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    add_str_html(html_name, '<p style="font-size:32px;"><b> %s, 0 vs risk positive fb, combined planar </b></p>' % (planar)) #3
    #title = 'norisk_vs_risk'
    add_str_html(html_name, '<h1 style="font-size:32px;"><b> 40 participants </b></h1>')
       
    for ch_num in range(len(chan_labels)):
        pic = chan_labels[ch_num] + '.jpeg'
        #(filename, pic, pic_folder, pos_n, size):
        add_pic_html(html_name, pic, pic_folder, pos[ch_num], [200,150])
   
    
    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    pdf_file = 'tf_plots_%s' % planar
    pdfkit.from_file(html_name, '/home/vera/MNE/time_frequency_plots/all_sensors/%s.pdf' % pdf_file, options=options)
print('\tAll printed')

'''
############################### В цикле ###################################
folders = ['norisk_vs_0', 'norisk_vs_prerisk', 'norisk_vs_risk', 'preisk_vs_0', 'risk_neg_vs_0', 'risk_pos_vs_0', 'risk_pos_vs_neg', 'risk_vs_0']
papki = ['2_40_step_2_time_bandwidth_by_default_4_early_log_comb_planar']

names = ['0_vs_norisk', 'norisk_vs_prerisk', 'norisk_vs_risk', '0_vs_preisk', '0_vs_risk_neg', '0_vs_risk_pos', 'risk_pos_vs_neg', '0_vs_risk']


for p in papki:    
    for idx, f in enumerate(folders):
        planars = ['{0}_{1}_ttest_no_fdr'.format(names[idx], p)] #1

        #папка откуда берем картинки
        pic_folder = '/home/vera/MNE/time_frequency_plots/{0}/{1}'.format(p, f) #2

        for ind, planar in enumerate(planars):
            #задаем имя нашей страницы
            html_name = "/home/vera/MNE/Paint_Nikita/topomaps_pdf/my.html"
            clear_html(html_name)
            add_str_html(html_name, '<!DOCTYPE html>')
            add_str_html(html_name, '<html>')
            add_str_html(html_name, '<body>')
            add_str_html(html_name, '<p style="font-size:32px;"><b> %s, %s </b></p>' % (names[idx], p)) #3
            #title = 'norisk_vs_risk'
            add_str_html(html_name, '<h1 style="font-size:32px;"><b> 40 participants </b></h1>')
               
            for ch_num in range(len(chan_labels)):
                pic = chan_labels[ch_num] + '.jpeg'
                #(filename, pic, pic_folder, pos_n, size):
                add_pic_html(html_name, pic, pic_folder, pos[ch_num], [200,150])
           
            
            add_str_html(html_name, '</body>')
            add_str_html(html_name, '</html>')
            pdf_file = 'tf_plots_%s' % planar
            pdfkit.from_file(html_name, '/home/vera/MNE/time_frequency_plots/2_40_step_2_time_bandwidth_by_default_4_early_log_comb_planar/all_sensors/%s.pdf' % pdf_file, options=options)
        print('\tAll printed')
