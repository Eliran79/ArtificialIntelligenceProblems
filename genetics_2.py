#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 12:50:58 2021

@author: Eliran Sabag
"""
from  functools import reduce
from operator import add, mul
import random


def list_sum(l):
    return reduce(add, l)

def list_prod(l):
    return reduce(mul, l)

def fitness_func(sum_set, mul_set):
    return abs(36-list_sum(sum_set)) + abs(360-list_prod(mul_set))

def reproduce(parent):
    #print('parent:', parent)
    sum_set, mul_set = parent
    idx = random.randint(0,4)
    print('Change index:{idx} for parent:{parent}'.format(idx=idx,parent=parent))

    sum_set_num = sum_set[idx]
    mul_set_num = mul_set[idx]

    sum_set[idx] = mul_set_num
    mul_set[idx] = sum_set_num

    return sum_set, mul_set

def mutate(child):
    sum_set, mul_set = child
    idx_left, idx_right = random.randint(0,4), random.randint(0,4)

    sum_set_num = sum_set[idx_left]
    mul_set_num = mul_set[idx_right]

    sum_set[idx_left] = mul_set_num
    mul_set[idx_right] = sum_set_num

    print('Mutate ({left},{right}) for child {child}'.format(left=idx_left,
                                                       right=idx_right,
                                                       child=child))
    return sum_set, mul_set


start_state = [[[1,2,3,4,5], [6,7,8,9,10]], [[10,9,8,7,6], [5,4,3,2,1]]]

def genetic_algorithm(population, fitness):
    while True:
        new_population = []
        for i in population:
            child = reproduce(i)
            if random.random()<0.1:
                child = mutate(child)
            new_population.append(child)

        for i in new_population:
            print('Individual:{}, Fitness:{}'.format(i, fitness_func(*i)))
            if fitness_func(*i)==0:
                return i

print('Best set:', genetic_algorithm(start_state, fitness_func))
