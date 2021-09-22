# для построения таймкурсов используюст данные усреденные внутри испытуемых. Например, которые можно получить с помощью скрипта evoked_ave_between_runs_and_fb_var3.py в случае если положительные и отрицательные FB рассматриваются вместе.

import mne
import numpy as np
import pandas as pd
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import os.path as op
import pdfkit
import statsmodels.stats.multitest as mul
from functions_tc import clear_html, add_str_html, to_str_ar, add_pic_html, full_fdr, plot_stat_comparison


################################################################################################################
####################################### Процесс построения ####################################################

# Задаем необходимые параметры
freq_range = 'alpha_8_12_trf_early_log'


# Координаты сенсоров лежат в файле MatLab, мы их вынимаем и берем только последние 102 значения
# которые соответствуют компайн планарам, первые 204 - это отвдельные планары
pos = io.loadmat('/home/vera/MNE/Paint_Nikita/pos_store.mat')['pos']
pos = pos[204:] # берем только последние 102, первые 204 - это отдельные планары
pos.shape

# Тоже самое и с названиями каналов
chan_labels_full = to_str_ar(io.loadmat('/home/vera/MNE/Paint_Nikita/channel_labels.mat')['chanlabels'])
chan_labels = chan_labels_full[204:] # берем только последние 102, первые 204 - это отдельные планары

#Условия сравнения
session = ["norisk", "prerisk"]
stim = ["resp"]

# Создаем или указываем папку куда будем сохранять рисунки
output = '/home/vera/MNE/Probability_learning/{0}/timecourses_{1}_{2}'.format(freq_range, session[0], session[1])
rewrite = True
os.makedirs(output, exist_ok=True)

#параметры функции plot_stat_comparison, используется ниже при использовании функции
label1 = session[0]
label2 = session[1]


subjects = pd.read_csv('/home/vera/MNE/Probability_learning/subj_list.csv')['subj_list'].tolist()

#path = os.getcwd() #текущая папка
#папка, откуда берем данные для построения тайм курсов
path = '/home/vera/MNE/Probability_learning/{0}_ave_into_subj'.format(freq_range)

# Задаем шаблон - любой Evoked
temp = mne.Evoked(os.path.join(path, "P001_norisk_evoked_{0}_resp.fif".format(freq_range)))

n = temp.data.shape[1]

#path_out = '/home/vera/MNE/Paint_Nikita/topomaps_pdf'
#задаем np.array со всеми 0. При этом 1200 это числов временных отчетов.
# его необходимо исправить если не будет совпадать с текущем
contr = np.zeros((len(subjects), 2, 102, n))

for ind, subj in enumerate(subjects):
    temp1 = mne.Evoked(os.path.join(path, "{0}_{1}_evoked_{2}_resp.fif".format(subj, session[0], freq_range)))
    temp1 = temp1.pick_types("grad")
    #contr[ind, 0, :204, :] = temp1.data
    contr[ind, 0, :, :] = temp1.data[::2] + temp1.data[1::2] # делаем комбайн планары
    temp2 = mne.Evoked(os.path.join(path, "{0}_{1}_evoked_{2}_resp.fif".format(subj, session[1], freq_range)))
    temp2 = temp2.pick_types("grad")

    #contr[ind, 1, :204, :] = temp2.data
    contr[ind, 1, :, :] = temp2.data[::2] + temp2.data[1::2] # делаем комбайн планары

comp1 = contr[:, 0, :, :]
comp2 = contr[:, 1, :, :]

t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)

#p_val fdr
p_val_fdr = full_fdr(p_val)

comp1_mean = comp1.mean(axis=0)
comp2_mean = comp2.mean(axis=0)


p_mul_max = 4
p_mul_min = -8

time = temp.times
#if False:
#    time = np.arange(-0.5, 0.05*(comp1_mean.shape[1])-0.5, 0.05)
#    print(time.shape)
#    print(comp1_mean.shape)
#else:
#    time = temp1.times[200:-200] - 2
print(time.shape)
print(comp1_mean.shape)
if rewrite:
    for indx in range(comp1_mean.shape[0]):
        #if indx < 204:
        #    p_mul = 0.3
        #else:
        #    p_mul = 0.6
        plot_stat_comparison(comp1_mean[indx], comp2_mean[indx], p_val[indx], p_val_fdr[indx], p_mul_max, p_mul_min, time, output, title = chan_labels[indx],
                             folder = f"{label1}_vs_{label2}", comp1_label = label1, comp2_label = label2)



    print('\tPictures generated')
else:
    print('\tPictures uploaded')


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
diction = {"w1c": "W1 (correct) (move)",
           "w2c": "W2 (correct) (move)",
           "w1em": "W1 (error) (move)",
           "w1eo": "W1 (error) (no move)",
           "d1cr": "D1 (correct) (no move)",
           "d2cr": "D2 (correct) (no move)",
           "d1fa": "D1 (error) (move)",
           "s1em": "S1 (error) (move)",
           "s1c": "S1 (correct) (move/nomove)",
           "s2c": "S2 (correct) (move/nomove)",
           'wlh2c': "active2 hicha correct move",
           'wrh2c': "active2 hivu correct move",
           'wlh1c': "active1 hicha correct move",
           'wrh1c': "active1 hivu correct move",
           "stim": "from stimulus ",
           "react": "from reaction ",
           "fb": "from feedback",
           "all": "from stimulus (all)",
           "st": "start",
           "end": "end"
           }


# С каким названием сохраниться рисунок. Список имел смысл, когда строили и отдельные планары и комбайны.
# сейчас в этом нет необходимости, но возможно придется вернуться и отдельным
planars = ['combine_planar_{0}_vs_{1}_{2}'.format(session[0], session[1], freq_range)]

#папка откуда берем картинки. Должно совпадать с тем куда мы их сохраняем, когда рисуем с помощью функции  
# plot_stat_comparison
pic_folder = output


for ind, planar in enumerate(planars):
    #задаем имя нашей страницы
    html_name = "/home/vera/MNE/Paint_Nikita/topomaps_pdf/my.html"
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    add_str_html(html_name, '<p style="font-size:32px;"><b> %s, average alpha 8-12; magenta p_val < 0.05(FDR); green p_val < 0.05 (without FDR) </b></p>' % (planar))
    #title = [diction[label1[:3]]  + " " + diction[label1[4:]], diction[label2[:3]]  + " " + diction[label2[4:]]]
    add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: blue;"> %s </span> vs <span style="color: red;"> %s </span> </b></p>' % (session[0], session[1]))
    #title = ['end', "soft-balanced"]
    #add_str_html(html_name, '<p style="font-size:32px;color:Maroon;"><b> %s %s </b></p>' % (title[0], title[1]))
    add_str_html(html_name, '<h1 style="font-size:32px;"><b> %s participants </b></h1>' % (contr.shape[0]))
    #add_str_html(html_name, '<h1 style="font-size:48px;"><b> (%s) </b></h1>' % 3)
    
    for ch_num in range(len(chan_labels)):
        pic = chan_labels[ch_num] + '.jpeg'
        #(filename, pic, pic_folder, pos_n, size):
        add_pic_html(html_name, pic, pic_folder, pos[ch_num], [200,150])
    '''
    if ind == 2:
        for ch_num in range(204, len(chan_labels)):
            pic = chan_labels[ch_num] + '.svg'
            
            #(filename, pic, pic_folder, pos_n, size):
    
            add_pic_html(html_name, pic, pic_folder, pos[ch_num], [200,150])
    else:
        for ch_num in range(ind, 204, 2):
            pic = chan_labels[ch_num] + '.svg'
            add_pic_html(html_name, pic,  pic_folder, pos[ch_num], [200,150])
    '''


    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    pdf_file = 'timecourse_%s' % planar
    print(path + '/%s' % html_name)
    pdfkit.from_file(html_name, '/home/vera/MNE/Probability_learning/alpha_8_12_trf_early_log/%s.pdf' % pdf_file, options=options)
print('\tAll printed')









