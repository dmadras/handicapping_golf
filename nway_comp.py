from readcsv import *
from sim_fns import *

def get_win_percentages(d, tiebreak_flag, bonus_strokes=0):
	'''Run simulations of various parameter sets on dataset d. Report winner counts
	and win percentages.'''
	#loop over allocation methods
	for style in ['diff', 'diff2']:
		#loop over difficulty orderings
		for ord_nm, order in (('diff', DIFFICULTY), ('emp_diff', EMP_DIFF), \
			                ('gap', GAP), ('best', BEST)):
			#simulate with these parameters
			r = sim_hdcp(d, style, L=order, tiebreak=tiebreak_flag, bonus=bonus_strokes)
			cts = win_ct_res(r) #count up wins, losses, etc from simulation
			print('{} {} {}: win: {}, loss: {}, tie: {}, win after tie: {}, loss after tie: {}'.format(\
		                style, ord_nm, str(bonus_strokes), str(cts['win']), str(cts['loss']), str(cts['tie']), str(cts['win-tie']), str(cts['loss-tie'])))
			print('{} {} {}: {}'.format(style, ord_nm, str(bonus_strokes), win_pct_res(r)))
