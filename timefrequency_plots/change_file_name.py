Когда создавались рисунки для каждого сенсора, то им присвоились номера Planar 1, а для TF_plots_all_sensors_probability.py необходимо присвоить название комбайн планаров.

import os
from scipy import stats, io
import re

# Меняем рабочую директорию, на ту, в которой лежат файлы, для которых будем менять название
os.chdir('/home/vera/MNE/time_frequency_plots/prerisk_vs_norisk')

# делаем список всех файлов в директории
a = os.listdir(path=".")

# функция для смены имени
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
 
for i in a:
    new_name = name_comb_planar(i)
    
    os.rename(i, new_name)       

