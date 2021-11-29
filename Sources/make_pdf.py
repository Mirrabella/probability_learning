

import os
import os.path as op
import numpy as np
import pdfkit

from functions import clear_html, add_str_html

# делаем папку для получившихся файлов
os.makedirs('/home/vera/MNE/Probability_learning/Sources/joint_pdf', exist_ok = True)

pic_folder = '/home/vera/MNE/Probability_learning/Sources/plot_sources_ttest_in_ave_int'

options = {
        'page-size':'A5',
        'orientation':'Landscape',
        'zoom': 1.0,
        'no-outline':None,
        'quiet':''
    }



var_of_plotting = ['pval_nofdr', 'pval_full_fdr', 'mean_beta']

#time_points = ['-0.8', '-0.7', '-0.6', '-0.5', '-0.4', '-0.3', '-0.2', '-0.1', '0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '2.0', '2.1', '2.2', '2.3']

time_points = ['before_resp', 'before_fb', 'after_fb']

# for feedback inside trial type
trial_types = ['norisk', 'risk', 'prerisk', 'postrisk']
for cond in trial_types:
    for v in var_of_plotting:
        
        #задаем имя нашей страницы
        html_name="/home/vera/MNE/Examples/my.html" #имя нашей страницы
        clear_html(html_name)
        add_str_html(html_name, '<!DOCTYPE html>')
        add_str_html(html_name, '<html>')
        add_str_html(html_name, '<body>')

        
        for t in time_points:
            #add_str_html(html_name, '<h1 align="left"  style= "font-size:80px">%s </h1>' % (cond))
            #add_str_html(html_name, '<h1 style="font-size:32px;"><b> 40 participants </b></h1>')
            pic = '{0}_{1}_neg_vs_pos_{2}.jpeg'.format(t, cond, v)
            add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic))
            #pic2 = '{0}'.format(cond) + '_space_fdr.jpeg'
            #add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic2))
            #pic3 = '{0}'.format(cond) + '_full_fdr.jpeg'
            #add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic3))
                 
        add_str_html(html_name, '</body>')
        add_str_html(html_name, '</html>')
        #pdf_file = 'tf_plots_%s' % planar
        pdfkit.from_file(html_name, '/home/vera/MNE/Probability_learning/Sources/joint_pdf/{0}_neg_vs_pos_{1}_ave_int.pdf'.format(cond, v), options=options)
        print('\tAll printed')

# for feedback inside trial type
trial_types = ['risk', 'prerisk', 'postrisk']
for cond in trial_types:
    for v in var_of_plotting:
        
        #задаем имя нашей страницы
        html_name="/home/vera/MNE/Examples/my.html" #имя нашей страницы
        clear_html(html_name)
        add_str_html(html_name, '<!DOCTYPE html>')
        add_str_html(html_name, '<html>')
        add_str_html(html_name, '<body>')

        
        for t in time_points:
            #add_str_html(html_name, '<h1 align="left"  style= "font-size:80px">%s </h1>' % (cond))
            #add_str_html(html_name, '<h1 style="font-size:32px;"><b> 40 participants </b></h1>')

            pic = '{0}_norisk_vs_{1}_{2}'.format(t, cond, v) + '.jpeg'
            add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic))
            #pic2 = '{0}'.format(cond) + '_space_fdr.jpeg'
            #add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic2))
            #pic3 = '{0}'.format(cond) + '_full_fdr.jpeg'
            #add_str_html(html_name, '<img src= %s />'%(pic_folder+'/'+pic3))
                 
        add_str_html(html_name, '</body>')
        add_str_html(html_name, '</html>')
        #pdf_file = 'tf_plots_%s' % planar
        pdfkit.from_file(html_name, '/home/vera/MNE/Probability_learning/Sources/joint_pdf/norisk_vs_{0}_{1}_ave_int.pdf'.format(cond, v), options=options)
        print('\tAll printed')

