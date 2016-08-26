from readcsv import *
from nway_comp import *

'''
This file contains a script for simulating various multiplicative bonuses.
Author: David Madras, 2016'''

d = readcsv('golfdata.csv')
outf = open('mult_bonus_results_small.csv', 'w')


outf.write('Handicapping Method,Ordering,Mult-bonus,Win Pctage,W,L,T,WT,LT\n')
for mb in np.arange(1.05, 1.11, 0.01):

	res = get_win_percentages_ret_results(d, tiebreak_flag=True, mult_bonus=mb)
	# for style in res:
	# 	outf.write('{},{},{},{},{},{},{},{}\n'.format(style, str(res[style]['mult_bonus']), str(res[style]['winpct']), str(res[style]['W']), str(res[style]['L']),\
	# 						str(res[style]['T']), str(res[style]['WT']), str(res[style]['LT'])))
	for k in res:
		style = k[0]; ordnm = k[1]
		outf.write('{},{},{},{},{},{},{},{},{}\n'.format(style, ordnm,str(res[k]['mult_bonus']), str(res[k]['winpct']), str(res[k]['W']), str(res[k]['L']),\
							str(res[k]['T']), str(res[k]['WT']), str(res[k]['LT'])))
outf.close()