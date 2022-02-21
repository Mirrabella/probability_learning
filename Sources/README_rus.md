**Более подробно про сам процесс подготовки stc файлов можно посмотреть** 
https://github.com/Mirrabella/MNE_processing/blob/main/Sources/Transform_from_sensors_to_sources.ipynb 

**Подготовка**

1. Визуально проверяем как прошла сегментация - segmentation_check.py. Если прошла  некорректно, то запускаем freeserfer еще раз

2. Создаем Head Model: BEM (boundary element model) surface - создается отдельно для каждого испытуемого — make_bem.py.

**Получение stc (Source Estimate) файлов**:

1. **Получение stc** для определенного частотного диапазона из  fif файлов. Есть 2 варианта в зависимости от задачи (получение stc для усреденных эпох либо отдельно для каждой эпохи (ненужное закомментировать):

**get_freq_stc.py**

*для получения stc отдельных эпох в functions.py есть два варианта функций: первый когда мы получаем stc из fif содержащих уже выделенную бету, либо (..._var2) получаем stc бэты для каждой эпохи отдельно подставляю эпохи в функцию mne.minimum_norm.source_band_induced_power в цикле, при этом с dSPM (by default) сигнал размазывается равномерно по всему мозгу, поэтому для уменьшения шума для отдельных эпох стоит применять sLoreta (method = 'sLoreta' в mne.minimum_norm.source_band_induced_power)  
https://mne.tools/stable/generated/mne.minimum_norm.source_band_induced_power.html   

Первый вариант судя по всему **НЕРАБОЧИЙ**

2. **Морфинг**
если получили усредненные stc: морфинг на fsaverage

**morph_stc.py**

если получили stc для отдлельных эпох: морфинг на fsaverage
**morph_stc_epo.py**

3. **Сохранение inverse operator для дальнейшего использования**

**inverse_operator_to_fif.py**

*в будущем сохранение  inverse operator можно прописать в саму функцию получения stc, чтобы не делать 2 раза одно и тоже.

4. **Усреднение**

4.1. Если получили отдельные эпохи — усредняем между эпохами:

**average_stc_in_epo.py**


4.2. Усреднение внутри испытуемого с разделением данных по фидбэкам

**stc_freq_ave_into_subjects.py**

без разделение по фидбекам

**united_of_fb.py**


4.3. Усреднение между испытуемыми

**stc_freq_ave.py**


5. **Ttest**

*подробнее по шагам Ttest_for_sources.ipynb*

5.1. ttest для различных контрастов. Усредение между временными точками делается с помощью resampling (example — resampling = 10, т. е. 10 точек в секунду, т. е. 1 точка это +/- 50 мс)

**ttest_sources.py**

5.2. ttest для различных контрастов. Усреднение между точками внутри временного интервала с помощью stc.mean()

**ttest_sources_ave_time_interval.py**


6. **Рисование**  

6.1. Рисование модели мозга fsaverage для 5.1 (усреднение с помощью resampling)

**plot_source.py**

6.2. Рисование модели мозга fsaverage для 5.2 (усреднение с помощью stc.mean())

**plot_source_ave_time_int.py**


7. **Сборка всех рисунков в pdf документ**

**make_pdf.py**

*промежуточный (вспомогательный) файл my.html, можно скачать, либо сделать самостоятельно
