from readcsv import *

d = readcsv('golfdata.csv')
##BOXPLOTS AND TABLES, FILTERED BY HDCP GROUP AND DIFFERENT HOLE ORDERINGS
	#headers = '{},{}\n'.format('Hdcp', ','.join([str(i) for i in range(1, 19)]))
	#mnfile = open('tables/means.txt', 'w')
	#sdfile = open('tables/sds.txt', 'w')
	#mnfile.write(headers); sdfile.write(headers)
for filt_name, hdcp_filt in [('all', lambda x: True)]:#, ('under10', lambda x: (x // 10) < 1),\
                             #('10to19', lambda x: (x // 10) == 1), ('20+', lambda x: (x // 10) > 1)]:
	ps = filter(lambda p: hdcp_filt(d[p]['hdcp']), list(d.keys()))
	all_holes = np.zeros((len(DIFFICULTY), len(ps)), dtype=np.int32)
	##ks = sorted(d.keys())
	for i in range(len(list(ps))):
		player = ps[i]
		for h in d[player]['holes']:
			all_holes[h - 1, i] = d[player]['holes'][h] - PARS[h - 1]
	
	##mns = np.mean(a, 0)
	##m = {i + 1:mns[i] for i in range(len(mns))}
	##emp_diff = sorted(list(m.keys()), key=lambda x: m[x], reverse=True)	
	
	a = np.transpose(all_holes)		
	plt.clf()
	for order_name, ordering in [('standard', list(range(1,19))), ('difficulty', DIFFICULTY), \
	                             ('emp_diff', EMP_DIFF), ('gap', GAP)]:
		
		i = np.array([ordering.index(i) + 1 for i in range(1, 19)]) - 1
		a2  = a[:, i]
		plt.boxplot(a2)
		plt.xticks(range(1,19), invert_list(ordering))
		plt.plot(range(1,19), np.mean(a2,0), 'rs')
		plt.xlabel('Hole Number')
		plt.ylabel('Strokes above par')
		#plt.title('Scores above par by Hole (Ordering: {}; Handicap: {})'.format(order_name, filt_name))
		plt.savefig('boxplots_redone/boxplot_{}_{}.png'.format(order_name, filt_name))	
		plt.close()
			
		##write means and sds to table
		#mns = np.mean(a, 0)
		#sds = np.std(a, 0)
		#mnrow = '{},{}\n'.format(filt_name, ','.join([str(i) for i in mns]))
		#sdrow = '{},{}\n'.format(filt_name, ','.join([str(i) for i in sds]))
		#mnfile.write(mnrow)
		#sdfile.write(sdrow)
	#mnfile.close()
	#sdfile.close()