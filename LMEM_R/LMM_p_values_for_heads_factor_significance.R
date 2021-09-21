#author: Ksenia Sayfulina

# save tables with p-values, which are used to build topomaps: white topomaps on which sensors with reliable significance of factors are marked

library(reshape2)
library(data.table)
library(ggplot2)
library(lme4)
# library("ggpubr")
library(emmeans)
library(lmerTest)
library(stringi)
library(stringr)
# install.packages("xlsx")
# library(xlsx)

# прописываем папку откуда беруться данные (path) и куда будут сохраняться полученные значения pvalue
path <- '/home/vera/MNE/Probability_learning/dataframe_for_LMEM_alpha_8_12_trf_early_log'
out_path <-'/home/vera/MNE/Probability_learning/dataframe_for_LMEM_alpha_8_12_trf_early_log/p_values_LMEM/'

#### prepare table with info ####
# sensors.csv - таблица где прописано соответсвие между порядковым номером сеносра и его обозначением (planar1)
sensor_info <- fread('/home/vera/MNE/Probability_learning/sensors.csv')
files <- data.table(full_filename=list.files(path, pattern = '*.csv', full.names = T))
files$short_filename <- list.files(path, pattern = '*.csv', full.names = F)
# files$short_filename <- gsub('planar1','',files$short_filename)

files[, sensor:=stri_extract_first_regex(short_filename,"[0-9]+")]
files[, interval:=str_extract(short_filename,'[0-9]+_[0-9]+.csv')]
files[,interval:=gsub('.csv','',interval)]
files$sensor <- as.integer(files$sensor)
files <- merge.data.table(files,sensor_info,by = c('sensor'))
files$effect <- NULL

## load subj_list ##
# список испытуемых
subj_list <- fread('/home/vera/MNE/Probability_learning/subj_list.csv')


#### make large table with p_values ####

temp <- fread(files[sensor==0]$full_filename)
temp$V1 <- NULL
cols <- colnames(temp)[grep('[0-9]',colnames(temp))]

######## for trial_type #############
p_vals <- data.table()
for (i in files$sensor){
  temp <- fread(files[sensor==i]$full_filename)
  temp$V1 <- NULL
  
  temp <- temp[subject %in% subj_list$subj_list]
  
  temp$subject <- as.factor(temp$subject)
  temp$round <- as.factor(temp$round)
  temp$feedback_cur <-as.factor(temp$feedback_cur)
  temp$feedback_prev <-as.factor(temp$feedback_prev)
  temp$scheme <-as.factor(temp$scheme)
  temp$trial_type <- as.factor(temp$trial_type)
  
  for (j in cols){
    m <- lmer(get(j) ~ trial_type*feedback_cur + (1|subject), data = temp)
    an <- anova(m)
    an <- data.table(an,keep.rownames = TRUE)
    an_cols <- c('rn','Pr(>F)') 
    an <- an[, ..an_cols]
    an$`Pr(>F)` <- format(an$`Pr(>F)`, digits = 3)
    an$interval <- j
    an$interval <- gsub('beta power','',an$interval)
    an <- dcast(an,formula = interval~rn,value.var = 'Pr(>F)')
    an$sensor <- i
    an$sensor_name <- files[sensor==i]$sensor_name
    p_vals <- rbind(p_vals,an)
  }
}

write.csv(p_vals,paste0(out_path, "p_vals_factor_significance_MEG.csv"))