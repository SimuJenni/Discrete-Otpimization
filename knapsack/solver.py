#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

        
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    # value, taken = inefficientSolution(capacity, len(items), items,  [0]*len(items))
    value = DP(capacity, items)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

# Very inefficient (but optimal!) recursive solution
def inefficientSolution(k, j, items, taken):
    if j == 0:
        return (0, taken)
    elif items[j-1].weight <= k:
        opt1 = inefficientSolution(k, j-1, items, taken)
        opt2 = inefficientSolution(k-items[j-1].weight, j-1, items, taken)
        if opt1[0]>=opt2[0]+items[j-1].value:
            taken[j-1] = 0
            return (opt1[0], taken)
        else:
            taken[j-1] = 1
            return (opt2[0]+items[j-1].value, taken)
    else:
        return inefficientSolution(k, j-1, items, taken)

import numpy as np

def DP(k, items):
    table = DPtable2(k, items)
    return table[k][len(items)]

def DPtable(k, items):
    table =[ [0 for x in range(len(items)+1)] for x in range(k+1)]
    weights = [item.weight for item in items]
    values = [item.value for item in items]
    for item in range(1, len(items)+1):
        for capacity in range(1, k+1):
            if weights[item-1]<=capacity:
                table[capacity][item] = max(table[capacity][item-1], table[capacity-weights[item-1]+1][item-1]+values[item-1])
            else:
                table[capacity][item] = table[capacity][item-1]
    return table

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

