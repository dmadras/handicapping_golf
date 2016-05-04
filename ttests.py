from readcsv import *
from sim_fns import *

def run_ttests(d, tiebreak_flag):
	'''Run simulations and t-test comparisons for various orders and handicapping
	allocation methods. Print results.'''
	res = {}
	#we'll filter out matches which don't fit certain criteria
	for filt_name, hdcp_filt in [('all', lambda x: True), ('under5', lambda x: (x // 5) < 1),\
		                     ('5to10', lambda x: (x // 5) == 1), ('10+', lambda x: (x // 5) > 1)]:
		for style in ('diff', 'diff2'):
			for dname, diff in (('Diff', DIFFICULTY), ('Emp_Diff', EMP_DIFF), ('gap', GAP)):
				print(style, dname)
				#run simulation with these parameters
				r = sim_hdcp(d, style, L=diff, tiebreak=tiebreak_flag, filt=hdcp_filt)
				winners = [r[m][5] for m in r] #who won each match: list of 1 or -1 (0 on tie)
				res[(filt_name, style, dname, 'wlt')] = winners
				windic = Counter(winners) #tally up how many of each
				print(windic)
				print(windic[1] / (float(windic[-1]) + float(windic[1]))) #this is the winning percentage
	
		#run t-tests on various parameter sets
		for dname in ('Emp_Diff', 'gap'):
			print('effect of {} given old hdcp, filter {}'.format(dname, filt_name))
			print(ttest_rel(res[(filt_name, 'diff','Diff','wlt')], res[(filt_name, 'diff',dname,'wlt')]))
			print('effect of {} given new hdcp, filter {}'.format(dname, filt_name))
			print(ttest_rel(res[(filt_name, 'diff2','Diff','wlt')], res[(filt_name, 'diff2',dname,'wlt')]))
			print('effect of new hdcp given {}, filter {}'.format(dname, filt_name))
			print(ttest_rel(res[(filt_name, 'diff',dname,'wlt')], res[(filt_name, 'diff2',dname,'wlt')]))
			print('effect of new hdcp given old Diff, filter {}'.format(filt_name))
			print(ttest_rel(res[(filt_name, 'diff','Diff','wlt')], res[(filt_name, 'diff2','Diff','wlt')]))
		
		print('effect of gap/Emp_Diff given old hdcp, filter {}'.format(filt_name))
		print(ttest_rel(res[(filt_name, 'diff','Emp_Diff','wlt')], res[(filt_name, 'diff','gap','wlt')]))	
		print('effect of gap/Emp_Diff given new hdcp, filter {}'.format(filt_name))
		print(ttest_rel(res[(filt_name, 'diff2','Emp_Diff','wlt')], res[(filt_name, 'diff2','gap','wlt')]))	
