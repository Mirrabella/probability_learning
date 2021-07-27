
###################### TF plots averange on every sensors (just as they are on the head) ############################

import mne
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import os.path as op
import pdfkit
import statsmodels.stats.multitest as mul

from functions import clear_html, add_str_html, to_str_ar, add_pic_html


####################### Задаем необходимые параметры ############################

# Создаем или указываем папку куда будем сохранять рисунки
output = '/home/vera/MNE/time_frequency_plots/all_sensors'
rewrite = True
os.makedirs(output, exist_ok=True)

# Координаты сенсоров лежат в файле MatLab, мы их вынимаем и берем только последние 102 значения
# которые соответствуют компайн планарам, первые 204 - это отвдельные планары
pos = io.loadmat('/home/vera/MNE/Paint_Nikita/pos_store.mat')['pos']
pos = pos[204:] # берем только последние 102, первые 204 - это отдельные планары
pos.shape

# Тоже самое и с названиями каналов
chan_labels_full = to_str_ar(io.loadmat('/home/vera/MNE/Paint_Nikita/channel_labels.mat')['chanlabels'])
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

# С каким названием сохраниться рисунок. Список имел смысл, когда строили и отдельные планары и комбайны.
# сейчас в этом нет необходимости, но возможно придется вернуться и отдельным
planars = ['norisk_vs_prerisk_comb_planar']

#папка откуда берем картинки
pic_folder = '/home/vera/MNE/time_frequency_plots/prerisk_vs_norisk'

for ind, planar in enumerate(planars):
    #задаем имя нашей страницы
    html_name = "/home/vera/MNE/Paint_Nikita/topomaps_pdf/my.html"
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    add_str_html(html_name, '<p style="font-size:32px;"><b> %s, norisk vs prerisk </b></p>' % (planar))
    title = 'norisk_vs_prerisk'
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


