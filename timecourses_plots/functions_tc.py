### Functions for drawing timecourses for each sensors and assembling them into a pdf file (like the sensors are located on the head).
### There is ttest statistics on timecourses


import mne
import numpy as np
import pandas as pd
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import os.path as op
import pdfkit
import statsmodels.stats.multitest as mul

########################################## Функции ################################################

# Очищаем pdf документ
def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

# функция, чтобы добавить текст (текстовое значение) в html документ
def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')



#преобразование данных в mat-файле в текстовые значения
def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp

# добавление рисунка на экран
# filename - название html файла в который мы будем размещать картинку
# pic - название картинки
# pic_folder - откуда берем картинку
# pos_n - позиция
# size - размер

def add_pic_html(filename, pic, pic_folder, pos_n, size):
    x = size[0]
    y = size[1]
    add_str_html(filename, '<IMG STYLE="position:absolute; TOP: %spx; LEFT: %spx; WIDTH: %spx; HEIGHT: %spx" SRC= %s />'%(round(y*(1-pos_n[1])*15,3), round(pos_n[0]*x*15,3), x, y, pic_folder+'/'+pic))
'''
#каким образом сформирвоать легенду. (Возможно рудимент, не знаю где пользуемся, проверить при доработке)
def get_label(session, stim):
    if "w" in stim[0] or "r" in stim[0]:
        sti = "w"
    elif "d" in stim[0]:
        sti = "d"
        
    return sti + session[6] + "c" + session[7:]
'''

# Full FDR -the correction is made once for the intire data array
def full_fdr(p_val_n):
    s = p_val_n.shape
    print(p_val_n.shape)
    pval = np.ravel(p_val_n)
    _, pval_fdr = mul.fdrcorrection(pval)
    pval_fdr_shape = pval_fdr.reshape(s)
    
    return pval_fdr_shape

# Далее главная функция , которая строит отдельные тайм курсы для каждого сенсора, в данном случае комбайн планара

# главная функция, она генерирует каждую отдельную картинку (в ней как раз придется менять цвета)
# comp1 - первый кондишен в нашем случае Актив 1
# comp2 - второй кондишен в нашем случае Актив 2
#path - куда сохраняем рисунк

def plot_stat_comparison(comp1, comp2, p_val, p_val_fdr, p_mul_max, p_mul_min, time, path, title='demo_title', folder='comparison',
                         comp1_label='comp1', comp2_label='comp2'):
    assert(len(comp1) == len(comp2) == len(time))
    plt.figure() #создаем рисунок 
    plt.rcParams['axes.facecolor'] = 'none' # делаем его прозрачным
    #plt.xlim(time[0], time[-1]) #назначаем границы рисунка по х
    plt.xlim(-1.6, 2.4)
    plt.ylim(p_mul_min, p_mul_max) #назначаем границы рисунка по у
    plt.plot([0, 0.001], [-9, 7], color='k', linewidth=3, linestyle='--', zorder=1) # вертикальная линия, которая показывает, где находится наше событие
    plt.plot([-6, 6], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1) # нулевая линия по горизонтали
    #plt.plot([2.6, 2.601], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1) #расположение фидбека
    #plt.axvline(0, color = 'k', linewidth = 3, linestyle = '--', zorder = 1)
    #plt.axhline(0, color = 'k', linewidth = 1.5, zorder = 1)
    #plt.axvline(2.5, color = 'k', linewidth = 3, linestyle = '--', zorder = 1)
    plt.plot(time, comp1, color='b', linewidth=3, label=comp1_label) # рисует график первого кондишена (всегда синий)
    plt.plot(time, comp2, color='r', linewidth=3, label=comp2_label) # рисует график второго кондишена (всегда красный)
    
    ##### Cледующие две строчки реализуют двух уровневую раскарску, которую необходимо будет менять ######
    
    
    # можно добавить в функцию еще один p_val - например pval и pval_fdr
    # цвет с FDR 0.65, 0.65, 0.65 - с FDR, без FDR нужно светлее
    plt.fill_between(time, y1 = p_mul_max, y2 = p_mul_min, where = (p_val < 0.05), facecolor = 'g', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul_max, y2 = p_mul_min, where = ((p_val_fdr < 0.05)), facecolor = 'm', alpha = 0.46, step = 'pre')
    
    
    plt.tick_params(labelsize = 16) # назначили размер подписей
    plt.legend(loc='upper right', fontsize = 16) # размер и расположение легенды
    plt.title(title, fontsize = 25) 
    #path = output # путь куда сохранять картинку
        
    # сохраняем в формате .svg,  это векторный формат, чтобы pdf весила поменьше
    # итоге я перестроила рисунки jpeg. Не заметила, чтобы весило больше, а проблем у меня оказалось меньше
    #plt.savefig(path+title + '.png', transparent=True)
    
    plt.savefig(op.join(path, title + '.jpeg'), transparent=True)
    plt.close()
