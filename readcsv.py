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

def invert_list(L):
	'''list of int -> list of int
	Turns handicap ordering indexed by course order to handicap ordering indexed by difficulty.
	If the course has 3 holes and the third is hardest, followed by the first and second, then
	the input would be L=[2,3,1] (the first index is the difficulty of hole 1),
	and the output would be L=[3,1,2] (the first index is the number of the hardest hole). This function
	also does the opposite.'''
	z = zip(L, range(1, len(L) + 1))
	z2 = sorted(z, key=lambda x: x[0])
	L_inv = [x[1] for x in z2]
	return L_inv


#The pars of each hole on our course. Hole is a par 5, etc
PARS =    [5,4, 3,4, 5, 4,5, 3,4,4, 5, 3,4, 4,5, 4, 3,4]

#These are various course orderings. The first number in the list is the 
#difficulty ranking of the first hole, the last number is the difficulty ranking
#of the last hole. E.g. in DIFFICULTY, hole number 1 is considered the 9th hardest.

#The course given difficulty ranking
DIFFICULTY = [9,5,17,1,11,15,3,13,7,4,10,16,2,14,6,12,18,8]
#The empirical difficulty ranking
EMP_DIFF = [18, 9, 8, 1, 17, 12, 10, 7, 5, 3, 16, 13, 2, 6, 15, 14, 11, 4]
#The gap difficulty ranking
GAP = [6, 12, 17, 9, 1, 11, 5, 18, 10, 3, 2, 14, 4, 15, 7, 13, 16, 8]
#an old optimized version
CLOSE_BEST = [12, 7, 2, 16, 14, 8, 13, 6, 3, 11, 17, 9, 15, 18, 1, 4, 10, 5]
BEST = CLOSE_BEST

def readcsv(fname):
	'''string -> dictionary with all the data in file fname
	Reads data from csv file fname. Keys are names of players.
	The value for each player contains a dictionary of the scores on all
	the holes, as well as that player's handicap.'''
	data = {}
	ct = 0 
	with open(fname) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			ct += 1 #to ensure uniqueness of keys for players with same name
			data[row['name'] + str(ct)] = row #reads row with headers as a dictionary
	for name in data:
		data[name]['holes'] = {}
		for k in data[name]:
			#set the keys in the holes dictionary to 1-18, the values to the scores on those holes
			if k != 'holes' and (data[name][k].isdigit() or\
			   data[name][k][0] == '-' and data[name][k][1:].isdigit()):
				data[name][k] = int(data[name][k])
				if k[0] == 'h' and k[1:].isdigit():
					data[name]['holes'][int(k[1:])] = data[name][k]
	return data


#To do:
#tiebreak re-do

if __name__ == '__main__':
	#plt.clf()
	d = readcsv('golfdata.csv')
	##four ball matches??? could be cool
	

	
	