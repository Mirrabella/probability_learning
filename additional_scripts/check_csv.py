import csv
t1 = open('/net/server/data/Archive/prob_learn/asmyasnikova83/CUR_FB/p_val_low_beta_12_20/analysis/p_vals_factor_significance_MEG.csv', 'r')
t2 = open('/net/server/data/Archive/prob_learn/asmyasnikova83/CUR_FB/p_val_low_beta_12_20/analysis/p_vals_factor_significance_MEG.csv', 'r')

#t2 = open('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/low_beta_12_20/p_values_LMEM/p_vals_factor_significance_MEG_beta_12_20.csv', 'r')
fileone = t1.readlines()
filetwo = t2.readlines()
t1.close()
t2.close()

outFile = open('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/low_beta_12_20/topomaps_line/test/check.csv', 'w')
x = 0
for i in fileone:
    if i != filetwo[x]:
        outFile.write(filetwo[x])
    x += 1
outFile.close()
