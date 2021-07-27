# Когда создавались рисунки для каждого сенсора, то им присвоились номера Planar 1, а для TF_plots_all_sensors_probability.py необходимо присвоить название комбайн планаров.

import os
from scipy import stats, io
import re
from functions import name_comb_planar

# Меняем рабочую директорию, на ту, в которой лежат файлы, для которых будем менять название
os.chdir('/home/vera/MNE/time_frequency_plots/prerisk_vs_norisk')

# делаем список всех файлов в директории
a = os.listdir(path=".")


 
for i in a:
    new_name = name_comb_planar(i)
    os.rename(i, new_name)       

