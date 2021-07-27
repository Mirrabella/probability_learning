

import os
from scipy import stats, io
import re


# функция для смены имени файла с TF plots для отдельного сенсора
def name_comb_planar(old_name):
    # разделяем строку по букве G (как в MEG0632.jpeg)
    b = re.split('G+', old_name)
    # получаем список из двух элементов берем 2ой, там где цифры и разделяем по точке, чтобы разделить разширение
    c = b[1].split(".")
    # берем первый элемент, где только цифры и делаем из них список, а затем делаем их числами (int())
    result = list(c[0])
    integer = []
    for i in result:
        integer.append(int(i))
        
    # увеличиваем четвертый элемент на 1 и убераем ненужный пятый (образовался при добавлении)
    integer.insert(3, (integer[3]+1))
    integer.pop()
    #Обратная операция - складываем все элементы в строку    
    string = []
    for i in integer:
        string.append(str(i))     
    string.insert(0, '+')
    myString = ''.join(string)
    d = old_name.split(".")
    d.insert(1, myString)
    d.insert(2, '.')
    new_name = ''.join(d)
    
    return(new_name)

#################### Рисование ###########################

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







