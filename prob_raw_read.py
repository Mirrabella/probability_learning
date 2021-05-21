subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   
        
#make date list
#date for 0 - 62 subjects
'''
date = ['161229', '161228', '170111', '170123', '170201', '170203', '170203', '170203', '170206', '170210', '170210', '170214',
       '170216', '170220', '170222', '170304', '170304', '170304', '170317', '170330', '170404', '170404', '170406', '170411',
       '170418', '170427', '170502', '170503', '170524', '170525', '170526', '170712', '170727', '170609', '170623', '170411', 
       '170330', '170310', '200807', '200819', '200824', '200731', '200805', '200805', '200807', '200819', '200824', '200829','200829', '201002', '201016', '201019', '201026', '201030', '201106', '201114', '201114', '201120', '201120', '201120', '201123', '201125', '201130', 
        '201130', '201204', '201204', '201204', '201205', '201205', '201205', '201209', '201218', '201218']
'''


rounds = [1, 2, 3, 4, 5, 6]

for idx, subj in enumerate(subjects):
	
	for r in rounds:
		raw_name = '{0}/{1}/ORIGINAL_TSSS/{0}_run{2}_raw_tsss_mc.fif'.format(subj, date[idx], r)
		raw_file = op.join(data_path, raw_name)
		raw = mne.io.Raw(raw_file, preload=True)


