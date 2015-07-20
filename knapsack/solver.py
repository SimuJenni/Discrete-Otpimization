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

    # value, taken = inefficientSolution(capacity, len(items), items,  [0]*len(items))
    value, taken = DP(capacity, items,  [0]*len(items))
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data    
    
def DP(k, items, taken):
    solution = [ [False for x in range(len(items)+1) ] for x in range(k+1)]
    table =[ [0 for x in range(2)] for x in range(k+1)]
    for item in items:
        for capacity in range(1, k+1):
            opt1 = table[capacity][item.index%2]
            if item.weight<=capacity:
                opt2 = table[capacity-item.weight+1][item.index%2]+item.value
                if opt1 >= opt2:
                    table[capacity][(item.index+1)%2] = opt1
                else:
                    table[capacity][(item.index+1)%2] = opt2
                    solution[capacity][item.index+1] = True
            else:
                table[capacity][(item.index+1)%2] = opt1
                
    value = table[k][len(items)%2]
    for i in range(len(items),0,-1):
        if not solution[k][i]:
            taken[i-1] = 0
        else:
            taken[i-1] = 1
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

