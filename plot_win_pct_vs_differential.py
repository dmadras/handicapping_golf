from sim_fns import *
import statsmodels.api as sm

'''
This file contains a script for plotting a figure of win percentage vs. handicap difference.
Author: David Madras, 2016'''

d = readcsv('golfdata.csv')
r = sim_hdcp(d, style='diff2', mult_bonus=1.08, tiebreak=True)
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

simdat = []
for i in range(25):
	for j in range(int(ttl_gameses[i])):
		simdat.append((hc_diffs[i], win_pcts[i]))


plt.clf()
s1 = [simdat[i][0] for i in range(len(simdat))]
s2 = [simdat[i][1] for i in range(len(simdat))]
plt.plot(s1, s2,  'g--')
p = np.poly1d(np.polyfit(s1, s2, 4))
xp = np.linspace(1, 25, 100)
plt.plot(xp, p(xp), 'r-')
plt.ylabel('Winning percentage')
plt.xlabel('Handicap differential ')
plt.ylim((0.44, 0.56))
plt.axhline(0.5, linestyle=':', color='b')
plt.savefig('hcdiff-winpct-smooth-differential-zero.png')



