# handicapping_golf

WARNING! I wrote this code many years ago as an undergrad - I make no promises as to its cleanliness or readability :)


deliverables.py - the main file to print out results

golfdata.csv - the data file

nway_comp.py - contains functions to simulate various handicapping schemes (name means N-way comparison - you can compare all the different methods easily after running this file)

random_comps.py - contains functions to test random orderings, as well as local search optimization for orderings

readcsv.py - contains data input file. Also contains all global constants for the program. This file is often imported by others.

sim_fns.py - contains many functions for simulating handicapping schemes and analyzing results. This file is often imported by others.

ttests.py - runs simulations on many different parameter settings, and then runs t-tests to compare for statistical significance.

