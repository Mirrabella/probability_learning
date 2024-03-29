I. How to use
II. Notes from discussion

I. How to use
There are 4 primary files: main.py, param.py, drop_components.py, cleaning_raw_ica.py.
In first you should set the necessary parameters in param.py, then use main.py, which return ica solution, and figures of properties of components for eyes movements and heart beats.Then you should select components, which you want to delete for every subject. After this you can use drop_components.py, which return cleaned raw with out bad components. If you would like to change some thing in ica cleaning process, see cleaning_raw_ica.py.

There are two exception:
1) L001 - haven't active3 in day1, but have "tail", from active2
2) L008 - have move1 and move2 in day 2 move session.

You can process the data separately (cleaning_L001_day1_active2-1_ICA.py, L001_day1_active2-1_drop_comp.py), or pre-connecting (cleaning_ica_conc.py, conc_drop_comp.py)

This scripts were used for ICA data cleansing of a new two-day experiment.  


The following components were droped (28.04.2020):
#day1 active1
#day1 active1
#components = [[1,21], [0, 3, 22], [9], [0,8], [0,8,32], [0,1,38], [0,2,11], [0,8], [0,4], [0,26], [0, 9,20], [0,17,33,50], [0,4,12], [0,7,12], [2,20], [0,22], [9,6,18], [0,37], [0,33], [2,28], [0, 3, 10], [0,14,18], [0,33], [0, 20], [0,37], [0, 12], [0,1,8], [0, 15, 17]]

#day1 passive1
#components = [[6,14], [0,1,22], [0,9,18], [0,12], [0,6], [1,3,17], [0,16], [0,8], [0,5], [0,12], [0, 4, 68], [0,21,26], [2, 0, 4], [0, 7, 17], [3,6],[0,25], [0,10,11], [0], [0,22], [13], [0,9,16], [0, 14], [0], [0, 19], [0,32], [0,5], [0,9,34], [0,5,25]]

#day1 passive2
#components  = [[12,9],[2, 1, 20], [0, 1, 12], [0,13], [0,3], [1, 7, 20], [0,22], [0], [0,4], [0, 21], [2,15], [0,16,37,55], [1,11], [0, 7,18], [0,9], [0,26], [0, 11, 14], [0], [0, 21], [1], [0, 8, 18], [0,20], [0, 32], [0, 18], [0, 33], [0,10], [0, 6, 44], [0,9]]

#day2 passive1
#components  = [[13], [0, 1, 9], [0, 1, 43], [0, 9], [0, 2, 46], [1, 0, 12], [0, 19], [0, 10], [0, 5], [0, 9], [0, 7, 11], [0, 11, 15], [0, 8, 27], [0, 4], [2, 18], [0, 20], [0, 13, 14], [0], [0, 20], [3, 39], [0, 12], [1, 16], [0], [0, 19], [0, 36], [0, 4, 17], [0, 11, 13], [0]]

#day2 passive2
#components  = [[11, 9], [0, 1, 40], [0, 1], [0, 10], [0 , 4], [1, 0, 16], [0, 26], [0, 11], [1, 5], [0, 15], [0, 7, 14], [0, 16], [0, 14], [1, 5, 23], [1, 7], [0, 23], [0, 13, 19], [0], [0, 15], [11, 44], [0, 50], [0, 14], [0], [1, 17], [0, 28], [1, 8, 20], [0, 8, 42], [0, 18]]

#day2 active1
#components  = [[2, 22], [0,3,13], [0, 1], [0,1,13], [0, 6],[0, 2, 18], [0, 25], [0, 1, 12], [0, 5], [0, 23], [0, 11, 27], [0, 3, 8], [3, 17, 23], [5, 2], [0, 27], [0, 28], [0, 20, 24], [0], [0], [0, 39], [0, 15, 41], [0, 21], [0], [0], [0, 43], [0, 8], [0, 5], [0, 14]]

#day2 active2
#components  = [[17], [0,1,4,21], [0, 1], [0, 13], [11], [0, 5, 29], [0, 2, 29], [0, 13], [0, 4], [0, 42], [0, 7], [0, 9, 16], [3, 15], [1, 22], [0, 25], [0, 23], [0, 25, 26], [0], [0, 21], [0, 21], [0,1, 46], [0,1,26], [0], [0, 31], [0, 41], [0, 18], [0, 12, 34], [0, 14]]

#day1 active2
#components  = [[1, 23], [0, 2, 26], [0, 7], [0, 13], [16], [0, 6, 29], [0, 32], [0, 12], [0, 8], [0, 23], [2, 6, 17], [0, 14, 31, 48], [5, 15], [0, 9, 17], [0, 24], [0, 29], [2, 19, 26], [0], [0, 20], [1], [1, 3, 15], [0, 18], [0], [0, 20], [0, 38], [0, 8], [0, 1, 3, 34], [0, 17]]

#day1 active3
#Attention: L001 was calculate separately
#components  = [[0, 1, 30], [0, 7, 22], [0, 15], [15], [0, 2, 16], [0, 33], [0, 14], [0, 6], [0, 25], [17], [0, 14, 31, 38], [6, 12], [0, 8, 17], [0, 31], [0, 25], [0, 16, 22], [0], [0, 19], [1], [0, 3, 9], [22], [0], [0, 23], [0, 39], [0, 22], [1, 2, 46], [0, 21, 29]]

#day1 active2-1
[37, 42]

#day1 move
#components  = [[0, 18], [0, 3], [0, 11], [7], [], [0, 1, 18], [0, 9, 47], [0, 4], [0, 4], [0, 15], [0, 13, 59], [0, 16, 19], [4, 11], [0, 4, 20], [0, 7], [0, 16], [0, 16, 18], [0], [0, 19], [5, 31], [0, 2, 8], [0, 17], [0], [0, 24], [0, 33], [0, 6], [0, 5, 26], [0, 10, 27]]

#day2 move
components  = [[2, 24], [0, 1], [2, 1, 15], [0, 8], [0, 2], [0, 1, 19], [0, 33], [0, 15], [0, 2, 3], [0, 30], [1, 9, 29], [0, 20], [8, 16, 20], [0, 2], [0, 23], [0, 10], [0, 19, 24], [0], [0, 10], [0, 31], [0, 17], [0, 21], [0], [0, 17], [1, 23], [0, 6], [0, 8], [0, 20]]

#

II Note from discussion

Из обсуждения с Викой Манюхиной, Аней Павловой и Борисом Владимировичем Чернышевым:

1)При недостаточном количестве компонент могут слипаться компоненты, соответствующие глазам и сердцу.
2)Fastica, Infomax - оба метода работают примерно одинаково на наших данных, Вика использовала в своей работе метод Fastica, поэтому остановимся на нем.
По словам Вики Манюхиной они не вычитали компоненты соответствующие горизонтальным саккадам, поскольку они довольно размазанные и не вносят большой вклад. Хотя Вика отмечает, что она рассматривали затылочную кору и возможно стоит пропробовать и так и так, в зависимости от задач. 
3)Поскольку в данном эксперименте 2 канала для вертикальных (EOG061 VEOG (левый глаз)) и горизонтальных (EOG062 HEOG) саккад строится два графика оценки компонент по корреляции вертикальным (верхний) и горизонтальным (нижний) саккадам.
4) Количество компонент выбирается исходя из количества независимых каналов - ранга (так выбирала Вика Манюхина). Число компонентов будет равно примерно 70.
5) При дальнейшем анализе решили вычитать один компонент соответствующий морганию и компоненты соответствующие сердечному ритму, так как чрезмерная чистка может привести к значительной потере данных.

Полезной функцией  является  plot_joint. Можно до начала использования ICA посмотреть как будут выглядеть компоненты для глаз и сердца.

Так же более подробную информация по методу ICA можно посмотреть в документации и примерах MNE и Jupyter notebook, который получился по результатам всех обсуждений (ICA_analysis.ipynb).



