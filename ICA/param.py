# Parameters for cleaning "Propability learning"


# data path, where raw data for cleaning are (change this if you need)
data_path = '/net/server/data/Archive/prob_learn/experiment'

#make the subjects list
a = ['P038']

for i in range(45,63):
    if i < 10:
        a += ['P00' + str(i)]
    else:
        a += ['P0' + str(i)]

# there is no data for L038 # for old cleaning
#a.remove('P038')

'''
b = [103, 104, 101, 102, 902, 901, 900]
c = []
for i in b:
    c += ['P' + str(i)]

d = [34,35,36]
e = []
for i in d:
    e += ['P0' + str(i)]

subjects = a + c + e
'''
subjects = a

# At the time of cleaning (27.08.20), number of subjects is 31

#make date list
#date for 0 - 30 subjects
'''
date = ['161229', '161228', '170111', '170123', '170201', '170203', '170203', '170203', '170206', '170210', '170210', '170214',
       '170216', '170220', '170222', '170304', '170304', '170304', '170317', '170330', '170404', '170404', '170406', '170411',
       '170418', '170427', '170502', '170503', '170524', '170525', '170526', '170712', '170727', '170609', '170623', '170411', 
       '170330', '170310', '200807', '200819', '200824']
'''
#date for 31 - 44 subjects without 38
#date = ['200731', '200805', '200805', '200807', '200819', '200824', '200829', '201002', '201016', '201019', '201026', '201030', '201106']

#date for 31 - 36
#date = ['200731', '200805', '200805', '200807', '200819', '200824']

#date for 37 - 44 without 38
#date = ['200829', '201002', '201016', '201019', '201026', '201030', '201106']

#date for 38, 45 - 62
date = ['200829', '201114', '201114', '201120', '201120', 
        '201120', '201123', '201125', '201130', 
        '201130', '201204', '201204', '201204', '201205', 
        '201205', '201205', '201209', '201218', '201218']


#if you don't need in all date, you can select apropriate
#date = date[0:3]

rounds = [1, 2, 3, 4, 5, 6]
# all rounds = [1, 2, 3, 4, 5, 6, 7, 'rest']




