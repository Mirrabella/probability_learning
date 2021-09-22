

import os
import os.path as op
import numpy as np
import pdfkit

from functions import clear_html, add_str_html

# делаем папку для получившихся файлов
os.makedirs('/home/vera/MNE/Probability_learning/topomaps_line_alpha_8_12_all/joint_pdf', exist_ok = True)

pic_folder = '/home/vera/MNE/Probability_learning/topomaps_line_alpha_8_12_all'

options = {
        'page-size':'A0',
        'orientation':'Landscape',
        'zoom':1.0,
        'no-outline':None,
        'quiet':''
    }

conditions = ['LMEM_feedback_cur_stat_alpha_8_12', 'LMEM_feedback_cur_stat_alpha_8_12_tb_2', 'LMEM_trial_type_feedback_cur_stat_alpha_8_12', 'LMEM_trial_type_feedback_cur_stat_alpha_8_12_tb_2', 'LMEM_trial_type_stat_alpha_8_12', 'LMEM_trial_type_stat_alpha_8_12_tb_2']

#conditions = ['LMEM_feedback_cur_stat_alpha_8_12']

for cond in conditions:

    #задаем имя нашей страницы
    html_name="/home/vera/MNE/Examples/my.html" #имя нашей страницы
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')

    add_str_html(html_name, '<h1 align="left"  style= "font-size:80px">%s </h1>' % (cond))
    
    #add_str_html(html_name, '<h1 style="font-size:32px;"><b> 40 participants </b></h1>')
    pic1 = '{0}'.format(cond) + '_no_fdr.jpeg'
    add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic1))
    pic2 = '{0}'.format(cond) + '_space_fdr.jpeg'
    add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic2))
    pic3 = '{0}'.format(cond) + '_full_fdr.jpeg'
    add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic3))
             
    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    #pdf_file = 'tf_plots_%s' % planar
    pdfkit.from_file(html_name, '/home/vera/MNE/Probability_learning/topomaps_line_alpha_8_12_all/joint_pdf/%s.pdf' % cond, options=options)
    print('\tAll printed')


