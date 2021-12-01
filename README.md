# Project name: probability_learning

***I. Частотно — временной анализ, построение рядов топомапов с отмеченными сенсорами, на которых влияние факторов достоверно.***

1.  **main.py** — используем скрипт для выделения целевых частот. См. functions.py для получения подробностей о процедуре. Тут важно учитывать особенности вычитания бейзлайна.

2. **comb_planar_save.py** — делаем combined planars из эпох (данные все еще остаются не усредненными)

3. **create_mem_table.py** — делаем таблицы для LMEM для combined planars, если мы хотим анализировать отдельные планары, то используем скрипт — create_mem_table_for_individual_planars.py

4. Переходим в R (скрипты подготовлены Ксенией Сайфулиной) — **LMEM_R/LMM_pvalues_for_heads_factor_significance.R** — в результате получаем таблицу знаменитостей факторов (и их взаимодействий) для каждого сенсора и для каждого временного интервала.

5. **plot_topomaps_line_signif_indiv_factors.py** — строим ряды топомапов для каждого из факторов (или их взаимодействия) без цветной заливки, и отмечаем на них сенсоры на которых этот фактор значим. 

6. **make_pdf_from_topomaps_line.py** — собираем полученные ряды топомапов в единый pdf файл 



***II. Построение цветных топомапов для контрастов с отмеченными значимыми сенсорами ( p value < 0.05)***

1.  **main.py** — используем скрипт для выделения целевых частот. См. functions.py для получения подробностей о процедуре. Тут важно учитывать особенности вычитания бейзлайна.
2.  **Усредение**
*в зависимости от того какой контраст планируется анализировать, можно применить следующие виды усредения*

2.1. **evoked_ave_between_runs_and_fb_var3.py** - усредняем данные сначала между блоками (run) и фидбеками, а затем внутри испытуемого
2.2. **evoked_ave_between_runs_var3_separ_fb.py** - усредняем данные внутри испытуемого, но фидбеки (положительный и отрицательные) оставляем разделенными




**combined_planar_average_into_subjects.py** - получение комбайн планаров из данных усредненных внутри испытуемого

**combined_planar_or_ind_planar_average_into_subjects.py** - практически повторяет предыдущий скрипт (**combined_planar_average_into_subjects.py**), но расширен тем, что можно получить и сохранить отдельно индивидуальные планары

**comb_planar_save.py** - make combined planars from EpochesTFR (see main.py) 

**create_mem_table.py** - collects data necessary for LMEM in a dataframe and stores it in .csv  

**create_mem_table_for_individual_planars.py** - практически повторяет предыдущий скрипт (**create_mem_table.py**), но в результае получаем табливцы .csv для LMEM для индивидуальных планаров

**evoked_ave_between_runs_and_fb_var3.py** - по итогу скрипта получаем усредненные данные внутри каждого испытуемого. Вначале объединяем данные для положительных фидбэков между блоками и усредняем их, затем тоже самое делаем для отрицательных фидбеков, затем соединяем данные по фидбеками и усредняем их с помощью mean внутри испытуемого, делаем Evoked с помощью донора, сохраняем.

**evoked_ave_between_runs_var3_separ_fb.py** - усредняем данные внутри испытуемого, но фидбеки (положительный и отрицательные) оставляем разделенными

**fix_cross_main.py** - finds fixation cross marks (needed to find a baseline) based on interest marks (e.g. response marks) 

**function.py** - functions, that may by  needed in the project .

**main.py** - make beta signal (epochs tfr) from raw 

**make_pdf_from_topomaps_lines.py** - размещаем ряды голов в одном pdf файле

**mio_cleaning_for_cond_events.py** - allows you to clear the labels of interest from the myogram (there is a general list of labels cleaned from artifacts and myogram and a list of labels broken down by conditions, we compare these two lists and if the labels from the list of interest are not in the list of labels cleared from the myogram, then we throw it out of the list marks of interest) 

**prob_raw_read.py** - script for reading rae data in probability learning project  

**prev_fb_save.py** - finds previous feedback marks (needed to LMEM) based on interest marks (e.g. response marks)   

**plot_topomaps_line_comb_planars.py** - в результате работы скрипта, получаем усредненные между испытуемыми данные, а так же линии топомапов со статистикой  для комбинированных планаров (используемые функции см. в function.py)

**plot_topomaps_line.py** - Так же как в предыдущем скрипте (**plot_topomaps_line_comb_planars.py**) в результате работы скрипта, получаем усредненные между испытуемыми данные, а так же линии топомапов со статистикой, но для любого типа планаров в цикле (используемые функции см. в function.py)

**plot_topomaps_line_LMEM_comb_planars.py** - в результате работы скрипта, получаем усредненные между испытуемыми данные, поделенные на необходимые временные интервалы и усредненные внутри этого интервала, а так же линии топомапов со статистикой LMEM (pvalue LMEM получают отдельно в R) для комбинированных планаров
 
**plot_topomaps_line_LMEM.py** - Так же как в предыдущем скрипте (**plot_topomaps_line_LMEM_comb_planars.py**), в результате работы скрипта, получаем усредненные между испытуемыми данные, поделенные на необходимые временные интервалы и усредненные внутри этого интервала, а так же линии топомапов со статистикой LMEM (pvalue LMEM получают отдельно в R), для любого типа планаров

**plot_topomaps_line_signif_of_indiv_factors.py** - в результате работы скрипта, строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Значипость факторов определяется по моделям LMEM  - pvalue LMEM получают отдельно в R.

**plot_timecourses.py** - построение grand average timecourses из данных усреденных внутри испытуемого

