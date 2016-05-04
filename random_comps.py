from readcsv import *
from sim_fns import *

def n_random_orders(d, n, style, tiebreak_flag):
	'''Run n simulations using n random difficulty orderings. style is a handicap
	allocation method, and tiebreak_flag indicates if we should do tiebreaks or not.'''
	res = {}
	#do n random orderings
	for i in range(n):
		a = list(range(1, 19)); random.shuffle(a) #new random order
		r = sim_hdcp(d, style, L=a, tiebreak=tiebreak_flag) #simulate
		res[(tuple(a))] = windics(r) #store the results
		print(win_pct(res[(tuple(a))][0])) #print the resultant winning percentage
	return res

def optimize_ordering_local_search(d, style, tiebreak_flag, start_n_random=0):
	'''Run local search in the space of orderings. If start_n_random is 0,
	use empirical difficulty ranking as starting seed. If not, try start_n_random
	different random orders, and take the best as your starting seed.
	style is a handicap allocation method, and tiebreak_flag indicates 
	if we should do tiebreaks or not.'''
	if start_n_random > 0: #choose starting seed ordering
		rand_res = n_random_orders(d, start_n_random, style, tiebreak_flag)
		start = list(sorted(rand_res.keys(), key=lambda x: win_pct(rand_res[x][0]))[0])
	else:
		start = EMP_DIFF[:]
	res = {}
	r = sim_hdcp(d, style, L=start, tiebreak=tiebreak_flag) #simulate with that ordering
	res[tuple(start)] = windics(r) #store that result
	best_so_far = win_pct(res[tuple(start)][0]) #it's our best so far
	print(start)
	print('starting at: ' + str(best_so_far))
	curr = start
	for i in range(1, 18): #iterate over all holes
		better = True
		while i >= 1 and better: #while we improve, swap holes
			ci = curr.index(i); ci1 = curr.index(i + 1) #which holes are i-th and i+1-th hardest?
			curr[ci], curr[ci1] = i + 1, i #swap them in the difficulty
			if not tuple(curr) in res: #if we haven't seen this ordering yet
				print(curr)
				print(i)				
				r = sim_hdcp(d, style, L=curr, tiebreak=tiebreak_flag) #simulate
				res[tuple(curr)] = windics(r) #store results
				wp = win_pct(res[tuple(curr)][0]) #get winning percentage
				if wp < best_so_far: #if it's better
					print('Improvement: ' + str(wp))
					best_so_far = wp #set it to our personal best
					i -= 1 #we'll try swapping this hole again
				else:
					curr[ci], curr[ci1] = i, i + 1 #if it's not better, swap back
					better = False
			else:
				curr[ci], curr[ci1] = i, i + 1 #if we've seen this ordering already, swap back
				better = False
	return res
