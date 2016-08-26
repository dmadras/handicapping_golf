from readcsv import *
from nway_comp import *

'''
This file contains a script for simluating handicaps with a piecewise bonus stroke method.
Author: David Madras, 2016'''

d = readcsv('golfdata.csv')
outf = open('piecewise_bonus_results.csv', 'w')

borders_differ = [3, 7, 21, 25]
bonuses_differ = [0.5, 1, 0.5, 0]
borders_cumul = [3, 7, 14, 21, 25]
bonuses_cumul = [0, 0.5, 1, 0.5, 0]
borders_differ_emp = [3, 7, 11,17, 25]
bonuses_differ_emp = [0.5,1,1.5,1,0.5]
borders_cumul_emp = [3, 7, 14, 21, 25]
bonuses_cumul_emp = [0, 0, 0, 0, 0]

borders_cumul_tiny = list(range(1, 26))
bonuses_cumul_tiny = [0,0.5,0,0.5,0.5,0.5,0.5,1,1,1,1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0,0,0,0]


def bonus_fn(x): #
	borders = borders_cumul
	bonus =  bonuses_cumul
	small_inds = filter(lambda i: x <= borders[i], range(len(borders)))
	b = bonus[min(small_inds)] if len(small_inds) > 0 else 0
	return b

for st_name, style in [('differential', 'diff'), ('cumulative', 'diff2')]:
	for ord_nm, order in [('std', DIFFICULTY), ('emp', EMP_DIFF), ('gap', GAP)]:
		# if not (st_name == 'cumulative' and ord_nm == 'std'):
		# 	continue
		r = sim_hdcp(d, style=style,  L=order, tiebreak=True, bonus_fn=bonus_fn)
		res = {}
		for k in r:
			hc_diff = r[k][0]; winner = r[k][5]
			if not hc_diff in res:
				res[hc_diff] = []
			res[hc_diff].append(winner)
		hc_diffs = []; win_pcts = []; ttl_gameses = []
		for k in sorted(res.keys()):
			ttl_wins = sum(map(lambda x: 1 if x == 1 else 0, res[k]))
			ttl_games = float(len(res[k]))
			win_pct = ttl_wins / ttl_games
			hc_diffs.append(k); win_pcts.append(win_pct); ttl_gameses.append(ttl_games)
		# print(hc_diffs)
		# print(win_pcts)
		# print(ttl_gameses)
		# for i in range(len(hc_diffs)):
		# 	print('Hdcp differential: {}, win pctage: {}, {} total matches'.format(hc_diffs[i], round(win_pcts[i], 3), int(ttl_gameses[i])))
		ttl_win_pctage = sum([win_pcts[i] * ttl_gameses[i] for i in range(len(win_pcts))]) / sum(ttl_gameses)
		print('{} {} {}'.format(st_name, ord_nm, str(ttl_win_pctage)))
		simdat = []
		for i in range(25):
			for j in range(int(ttl_gameses[i])):
				simdat.append((hc_diffs[i], win_pcts[i]))


		plt.clf()
		s1 = [simdat[i][0] for i in range(len(simdat))]
		s2 = [simdat[i][1] for i in range(len(simdat))]
		plt.plot(s1, s2,  'g--')
		# lowess = sm.nonparametric.lowess(s2, s1, frac=0.1)
		# plt.plot(lowess[:, 0], lowess[:, 1])
		p = np.poly1d(np.polyfit(s1, s2, 4))
		xp = np.linspace(1, 25, 100)
		plt.plot(xp, p(xp), 'r-')
		plt.ylabel('Winning percentage')
		plt.xlabel('Handicap differential ')
		plt.ylim((0.44, 0.56))
		plt.axhline(0.5, linestyle=':', color='b')
		plt.savefig('hcdiff_figs/hcdiff-winpct-smooth-piecewise-{}-{}.png'.format(st_name, ord_nm))
		# plt.savefig('hcdiff_figs/hcdiff-winpct-smooth-piecewise-{}-{}-everyhole.png'.format(st_name, ord_nm))


