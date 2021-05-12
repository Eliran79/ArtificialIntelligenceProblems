#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:22:44 2021

@author: Eliran Sabag
"""

# genetic algorithm search of the one min optimization problem
from numpy.random import randint
from numpy.random import rand

import random

import numpy as np

# objective function
def fitness_func(individual):

    sum_set = individual[:5]
    mul_set = individual[5:]

    return np.abs(36-sum_set.sum())+np.abs(360-np.prod(mul_set))

# tournament selection
def selection(pop, scores, k=3):
	# first random selection
    selection_ix = randint(len(pop))
    #print(selection_ix)
    #print(pop)
    for ix in randint(0, len(pop), k-1):
		# check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
	# check for recombination
    if rand() < r_cross:
		# select crossover point that is not on the end of the string
        pt = randint(1, len(p1)-2)

        if (p1[pt] not in np.hstack([p2[:pt], p2[pt+1:]]) and
            p2[pt] not in np.hstack([p1[:pt], p1[pt+1:]])):
        # perform crossover
            c1[pt] = p2[pt]
            c2[pt] = p1[pt]
    return [c1, c2]

# mutation operator
def mutation(child, r_mut):

    if rand() < r_mut:
        idx1, idx2 = random.randint(0,9), random.randint(0,9)

        sum_set_num = child[idx1].copy()
        mul_set_num = child[idx2].copy()

        child[idx1] = mul_set_num
        child[idx2] = sum_set_num

    return child

# genetic algorithm
def genetic_algorithm(objective, pop, n_iter, n_pop, r_cross, r_mut):
    # initial population of random bitstring
    # pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop)]
    # keep track of best solution
    best, best_eval = 1E6, objective(pop[0])
    # enumerate generations
    for gen in range(n_iter):
        # evaluate all candidates in the population
        scores = [objective(c) for c in pop]
        # check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))
        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # crossover and mutation
            #print('*',p1,p2)
            for c in crossover(p1, p2, r_cross):
                #print('**',c)
                c = mutation(c, r_mut)
                # store for next generation
                children.append(c)
        # replace population
        pop = children
    return [best, best_eval]

# define the total iterations
n_iter = 100
# define the population size
n_pop = 10
# crossover rate
r_cross = 0.9
# mutation rate
r_mut = 0.1 #1.0 / float(n_bits)

rng = np.random.default_rng()
# Initial population
pop = np.array([rng.choice(np.arange(1,11),replace=False, size=10) for _ in range(n_pop)])
# perform the genetic algorithm search


best, score = genetic_algorithm(fitness_func, pop, n_iter, n_pop, r_cross, r_mut)
print('Done!')
print('f(%s) = %f' % (best, score))
