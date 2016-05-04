#put all functions in here for final product
#want one click results

from ttests import *
from nway_comp import *
from random_comps import *

d = readcsv('golfdata.csv')

#t-tests, with tiebreak (remember to go back to old tiebreak method)
run_ttests(d, tiebreak_flag=True)

#get all win pctages - base
get_win_percentages(d, tiebreak_flag=True)

#bonus stroke tests
for b in (0.5, 1, 2):
    get_win_percentages(d, tiebreak_flag=True, bonus_strokes=b)

#random optimization
res = optimize_ordering_local_search(d, 'diff', tiebreak_flag=True, start_n_random=100)
ord1 = sorted(res.keys(), key=lambda x: win_pct(res[x][0]))
print('Best order for old hdcp (w/ tiebreak) is: {}, win pct {}'.format(str(ord1[0]), str(win_pct(res[ord1[0]][0]))))
ord1for50 = sorted(res.keys(), key=lambda x: abs(win_pct(res[x][0]) - 0.5))
print('Fairest order for old hdcp (w/ tiebreak) is: {}, win pct {}'.format(str(ord1for50[0]), str(win_pct(res[ord1for50[0]][0]))))


res = optimize_ordering_local_search(d, 'diff2', tiebreak_flag=True, start_n_random=100)
ord2 = sorted(res.keys(), key=lambda x: win_pct(res[x][0]))
print('Best order new hdcp (w/ tiebreak) is: {}, win pct {}'.format(str(ord2[0]), str(win_pct(res[ord2[0]][0]))))
ord2for50 = sorted(res.keys(), key=lambda x: abs(win_pct(res[x][0]) - 0.5))
print('Fairest order for new hdcp (w/ tiebreak) is: {}, win pct {}'.format(str(ord2for50[0]), str(win_pct(res[ord2for50[0]][0]))))

for (style, order, ord_nm) in [('diff', ord1[0], 'optimized1 with tiebreak'),\
                               ('diff2', ord2[0], 'optimized2 with tiebreak'),\
                               ('diff', ord1for50[0], 'fair-optimized1 with tiebreak'), \
                               ('diff2', ord2for50[0], 'fair-optimized2 with tiebreak')]:
    r = sim_hdcp(d, style, L=order, tiebreak=True, bonus=0)
    cts = win_ct_res(r)
    print(order)
    print('{} {} : win: {}, loss: {}, tie: {}, win after tie: {}, loss after tie: {}'.format(\
                                    style, ord_nm, str(cts['win']), str(cts['loss']), str(cts['tie']), str(cts['win-tie']), str(cts['loss-tie'])))
    print('{} {}: {}'.format(style, ord_nm,  win_pct_res(r)))


