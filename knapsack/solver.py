#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
#from numba import jit,uint32,int32
#import numpy as np

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
    
    #value, taken = DP(capacity, items)
    value, taken = BnB(capacity, items)

    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data    

def BnB (k, items):
    items = sorted(items, key = lambda x: float(x.value)/x.weight)
    Node = namedtuple("Node", ['value', 'room', 'est', 'idx', 'taken'])
    fringe = []
    taken =  {}
    fringe.append(Node(0, k, estimate(items, 0, 0, k),0, {}))
    done = False
    bestVal = 0
    
    while fringe:
        state = fringe.pop()
        if state.est < bestVal:
            break
        if state.idx >= len(items):
            continue
        est1 = estimate(items, state.idx+1, state.value, state.room)
        node1 = Node(state.value,state.room, est1, state.idx+1, state.taken)
        if items[state.idx].weight <= state.room:
            newVal = state.value+items[state.idx].value
            bestVal = max(newVal, bestVal)
            takenWith = set(state.taken)
            takenWith.add(state.idx)
            newRoom = state.room - items[state.idx].weight
            est2 = estimate(items, state.idx+1, newVal, newRoom)
            node2 = Node(newVal, newRoom, est2, state.idx+1, takenWith)
            if est2 >= est1:
                fringe.append(node2)
                fringe.append(node1)
            else:
                fringe.append(node1)
                fringe.append(node2)
        else:
            fringe.append(node1)

    return bestVal, []
        


def estimate(items, idx, value, room):
# Optimistic estimate for BnB algorithm
    est = value
    for i in range(idx, len(items)):
        item = items[i]
        if room >= item.weight:
            est += item.value
        else:
            est += item.value*room/item.weight
            return est
        idx += 1
    return est

def DP(k, items):
    items = sorted(items, key = lambda x: x.weight)    
    solution = [ [False for x in range(len(items)+1) ] for x in range(k+1)]
    table =[ [0 for x in range(2)] for x in range(k+1)]
    #table = np.zeros((len(items), k), dtype=np.int32)
    i=0
    for item in items:
        for capacity in range(item.weight, k+1):
            opt1 = table[capacity][i%2]
            if item.weight<=capacity:
                opt2 = table[capacity-item.weight+1][i%2]+item.value
                if opt1 >= opt2:
                    table[capacity][(i+1)%2] = opt1
                else:
                    table[capacity][(i+1)%2] = opt2
                    solution[capacity][i+1] = True
            else:
                table[capacity][(i+1)%2] = opt1
        i+=1
    value = table[k][len(items)%2]

    taken =  [0]*len(items)
    for i in range(len(items),0,-1):
        if solution[k][i]:
            taken[items[i-1].index] = 1
            k -= items[i-1].weight        
            
    return value, taken

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

