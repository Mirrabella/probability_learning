# probability_learning

**prob_raw_read.py** - script for reading rae data in probability learning project  

**function.py** - functions, that may by  needed in the project 

**mio_cleaning_for_cond_events.py** - allows you to clear the labels of interest from the myogram (there is a general list of labels cleaned from artifacts and myogram and a list of labels broken down by conditions, we compare these two lists and if the labels from the list of interest are not in the list of labels cleared from the myogram, then we throw it out of the list marks of interest) 

**fix_cross_main.py** - finds fixation cross marks (needed to find a baseline) based on interest marks (e.g. response marks) 

**main.py** - make beta signal (epochs tfr) from raw 

**comb_planar_save.py** - make combined planars from EpochesTFR (see main.py) 

**prev_fb_save.py** - finds previous feedback marks (needed to LMEM) based on interest marks (e.g. response marks)   

**create_mem_table.py** - collects data necessary for LMEM in a dataframe and stores it in .csv  

**create_mem_table_for_individual_planars.py** - практически повторяет предыдущий скрипт (**create_mem_table.py**), но в результае получаем табливцы .csv для LMEM для индивидуальных планаров

**grand_average_v1.py** - average the values using mne.grand_average() (average var. 1)   

**evoked_ave_between_runs_and_fb.py** - по итогу скрипта получаем усредненные данные внутри каждого испытуемого. Усреденение происходит средствами MNE: сначала усредняем данные внутри фидбека (и внутри блока (run)), т.е. из эпох получаем evoked. Затем собираем список evoked для каждого испытуемого (должно получаеться от 0 до 12, по количеству блоков 6, каждый блок разделен на 2 фид бека - 12), затем получаем grand_averange из списка evoked, с помощью функции mne.grand_averege()  

**evoked_ave_between_runs_and_fb_var2.py** - по итогу скрипта получаем усредненные данные внутри каждого испытуемого. Вначале объединяем данные для разных фидбэков внутри блока, затем усредняем их с помощью mean. Далее объединяем данные для испытуемого в один массив и усредняем их с помощью mean, делаем Evoked с помощью донора, сохраняем.

**evoked_ave_between_runs_and_fb_var3.py** - по итогу скрипта получаем усредненные данные внутри каждого испытуемого. Вначале объединяем данные для положительных фидбэков между блоками и усредняем их, затем тоже самое делаем для отрицательных фидбеков, затем соединяем данные по фидбеками и усредняем их с помощью mean внутри испытуемого, делаем Evoked с помощью донора, сохраняем.

**plot_topomaps_line_comb_planars.py** - в результате работы скрипта, получаем усредненные между испытуемыми данные, а так же линии топомапов со статистикой  для комбинированных планаров (используемые функции см. в function.py)

**plot_topomaps_line.py** - Так же как в предыдущем скрипте (**plot_topomaps_line_comb_planars.py**) в результате работы скрипта, получаем усредненные между испытуемыми данные, а так же линии топомапов со статистикой, но для любого типа планаров в цикле (используемые функции см. в function.py)

**plot_topomaps_line_LMEM.py** - в результате работы скрипта, получаем усредненные между испытуемыми данные, поделенные на необходимые временные интервалы и усредненные внутри этого интервала, а так же линии топомапов со статистикой LMEM (pvalue LMEM получают отдельно в R)

**plot_topomaps_line_signif_of_indiv_factors.py** - в результате работы скрипта, строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Значипость факторов определяется по моделям LMEM  - pvalue LMEM получают отдельно в R.

**combined_planar_average_into_subjects.py** - получение комбайн планаров из данных усредненных внутри испытуемого

**combined_planar_or_ind_planar_average_into_subjects.py** - практически повторяет предыдущий скрипт (**combined_planar_average_into_subjects.py**), но расширен тем, что можно получить и сохранить отдельно индивидуальные планары

**plot_timecourses.py** - построение grand average timecourses из данных усреденных внутри испытуемого

