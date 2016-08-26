import csv
import sys
from collections import Counter
import random
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, ttest_rel
import sys
from readcsv import *

'''
This file contains functions necessary for simulating play outcomes with various handicaps.
Author: David Madras, 2016'''

def play_hole(style, sc1, sc2, h1, h2, holenum, offset=0, L=DIFFICULTY,p1='', p2=''):
	'''Simulate the play on a hole. Style is handicapping allocation method.
	sc1 is better player's score, sc2 is worse players' score. h1 and h2
	are the handicaps. holenum is 1-18, the number on the course. If offset > 0,
	we start handicapping at a hole other than 1.'''
	hc = abs(h1 - h2); hf = hc % 1 #for half stroke bonuses
	#base: the number of strokes we give on every hole
	base = int(hc / 18)
	#border: the hole difficulty number at which we stop giving strokes
	border = int(hc % 18)
	#scbet: score of better player, scwor: score of worse player
	scbet = sc1
	if holenum > 18: #in a tiebreak, treat hole 19 like hole 1, etc.
		holenum = holenum - 18
	#old handicap tiebreaker procedure
	#if holenum > 18 and style != 'no':
		#scwor = sc2 - base
		##then elif below, not if
	if style == 'no': #no handicap
		scwor = sc2
	elif style == 'dumb': #take course ordering as difficulty ordering
		scwor = sc2 - base - (1 if holenum <= border else 0)
	elif style == 'diff':
		#this is the standard method of handicap allocation
		#on difficulty ordering, always start at 1
		#always subtract the base amount
		#if our difficulty ranking is less than the "border" (difference in handicap % 18)
			#subtract an extra stroke, half if we're just over the border and a half stroke is indicated
		scwor = sc2 - base - \
		        (hf if (L[holenum - 1] - offset - 1) % 18 == border else 0)	- \
		        (1 if (L[holenum - 1] - offset - 1) % 18 \
		                      <= border - 1 else 0)
	elif style == 'diff2':
		#this is our proposed method of handicap allocation
		#same as above except we offset our starting hole by h1, the better players' handicap
		h1 = min(h1, h2)
		# inth1 = int(h1); inth2 = int(h2)
		# hc = abs(inth1 - h2); border = int(hc % 18); base = int(hc / 18)
		# scwor = sc2 - base - \
		#         (hfwor if (L[holenum - 1] - h1 - offset - 1) % 18 == border else 0)	- \
  #                               (1 if (L[holenum - 1] - h1 - offset - 1) % 18 \
		#                  <= border - 1 else 0)			
		scwor = sc2 - base - \
        (hf if (L[holenum - 1] - h1 - offset - 1) % 18 == border else 0)	- \
                        (1 if (L[holenum - 1] - h1 - offset - 1) % 18 \
                 <= border - 1 else 0)			
	diff =  scbet - scwor
	if diff < 0: #better player won
		win = 1
	elif diff > 0: #worse player won
		win = -1
	else: #tied
		win = 0
	return scbet, scwor, diff, win
	
def sim_hdcp(d, style, offset=0, L=DIFFICULTY, tiebreak=False, filt=lambda x: True, bonus=0, mult_bonus=1, \
							stroke_play=False, bonus_fn=lambda hc: 0):
	'''Simulate handicapping method with these parameters; style is old ('diff') 
	or new ('diff2') handicap allocation methods, offset is 0 to 17, L is difficulty ordering,
	tiebreak False indicates no tiebreaking procedure followed (ignore ties), filt determines 
	which absolute differences in handicap we will use.'''
	
	results = {} #to store match results
	players = sorted(list(d.keys()))
	for i in range(len(players)):
		for j in range(i + 1, len(players)):
			#we'll simulate a match between players i and j
			p1 = players[i]; p2 = players[j]
			h1 = d[p1]['hdcp']; h2 = d[p2]['hdcp'] #the players' handicaps
			hc = abs(h1 - h2)
			if not filt(hc): #we only want certain handicap differences
				continue
			h1 = round(h1 * mult_bonus); h2 = round(h2 * mult_bonus)
			if h1 > h2:
				better = p2; worse = p1 #p2 has a lower handicap, is the favoured player
				h1 += bonus #add bonus strokes to worse player, if desired
				h1 += bonus_fn(hc)
			elif h2 > h1:
				better = p1; worse = p2
				h2 += bonus
				h2 += bonus_fn(hc)
			else: #if handicaps are equal, it's irrelevant to our analysis.
				continue	
			res = {} #to store results of holes for this match
			if stroke_play:
				better_player_ttl = sum([d[better]['holes'][h] for h in d[better]['holes']])
				worse_player_ttl = sum([d[worse]['holes'][h] for h in d[worse]['holes']])
				ttl_diff = better_player_ttl - worse_player_ttl
				adj_ttl_diff = ttl_diff + hc
				if adj_ttl_diff > 0:
					winner = -1
				elif adj_ttl_diff < 0:
					winner = 1
				else:
					winner = 0
				results[(better, worse)] = (hc, (better_player_ttl, worse_player_ttl), None, h1, h2, winner)
			else:	
				for h in d[better]['holes']:
					holenum = int(h)
					#simulate the hole with these players' scores
					scbet, scwor, diff, win = \
					        play_hole(style, d[better]['holes'][h], d[worse]['holes'][h],\
					                  h1, h2, holenum, offset, L, p1=p1, p2=p2)
					res[h] = (scbet, scwor, diff, win) #store their scores, the margin of victory, and 1 for favoured player win, 0 for tie, -1 for upset.
				wins = [res[h][-1] for h in sorted(res.keys())] #the results for each hole
				if sum(wins) > 0:
					winner = 1 #the better player won more holes
				elif sum(wins) < 0:
					winner = -1 #the worse player won more holes
				elif sum(wins) == 0: #they won the same number of holes
					if not tiebreak:
						winner = 0 #call it a tie
					else:
						tied = True
						hole = 1
						while tied and hole <= 18: #we'll simulate the rest of the course again, if necessary
							scbet, scwor, diff, win = \
								play_hole(style, \
								d[better]['holes'][hole],\
								d[worse]['holes'][hole],h1,h2, 19, offset, L)
							if win != 0:
								tied = False #we have a winner
							hole += 1
						if hole > 18:
							print('{},{}: players tied on every hole - flipping a coin'.format(p1, p2))
							winner = random.randint(0,1) #only if they get the same score on every hole - doesn't happen in our dataset, very unlikely
						else:
							winner = win #1, -1, 0 for better win, worse win, tie
				results[(better, worse)] = (hc, res, wins, h1, h2, winner) #store results of match		
	return results	


def win_ct_res(r):
	'''Return dictionary summarizing match results from r:
	How many wins, losses, ties, wins in tiebreak, and loss in tiebreak were
	experienced by the favoured player.'''
	cts = {'win':0, 'loss':0, 'tie':0, 'win-tie': 0, 'loss-tie': 0}
	results = [r[k][2] for k in r] #the hole by hole results for each match
	winners = [r[k][5] for k in r] #the final result for each match
	movs = [sum(res) for res in results] #margins of victory for each match
	for i in range(len(winners)):
		if movs[i] > 0:
			cts['win'] += 1
		elif movs[i] < 0:
			cts['loss'] += 1
		else: #movs = 0, tie after 18 holes
			if winners[i] == 1:
				cts['win-tie'] += 1
			elif winners[i] == -1:
				cts['loss-tie'] += 1
			else: #there was no tiebreak
				cts['tie'] += 1
	return cts

def win_pct(d):
	'''Calculate wins/losses from a dictionary with 2 keys: 1 and -1, representing
	wins and losses by the favoured player.'''
	return d[1] / (float(d[-1]) + float(d[1]))

def win_pct_res(r):
	'''Calculates win percentage of favoured player directly from the output of sim_hdcp.'''
	windic, windic_nt = windics(r)
	return win_pct(windic_nt)

def windics(r):
	'''Make 2 dictionaries: one counting the wins, losses and ties, one just
	counting wins and losses. Return both. This function takes the output of 
	sim_hdcp as input.'''
	num = float(len(r))
	movs = [sum(r[m][2]) for m in r]
	winners = [r[m][5] for m in r]; winners_nt = winners
	windic = Counter(winners)
	windic_nt = Counter(winners_nt)
	return (windic, windic_nt)
