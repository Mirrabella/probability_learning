# probability_learning

**prob_raw_read.py** - script for reading rae data in probability learning project  

**function.py** - functions, that may by  needed in the project 

**mio_cleaning_for_cond_events.py** - allows you to clear the labels of interest from the myogram (there is a general list of labels cleaned from artifacts and myogram and a list of labels broken down by conditions, we compare these two lists and if the labels from the list of interest are not in the list of labels cleared from the myogram, then we throw it out of the list marks of interest) 

**fix_cross_main.py** - finds fixation cross marks (needed to find a baseline) based on interest marks (e.g. response marks) 

**main.py** - make beta signal (epochs tfr) from raw 

**comb_planar_save.py** - make combined planars from EpochesTFR (see main.py) 

**prev_fb_save.py** - finds previous feedback marks (needed to LMEM) based on interest marks (e.g. response marks)   

**create_mem_table.py** - collects data necessary for LMEM in a dataframe and stores it in .csv  

**grand_average_v1.py** - average the values using mne.grand_average() (average var. 1)
