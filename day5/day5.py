# https://adventofcode.com/2023/day/5

import re

input = open('day5/day5_0.txt', 'r')
almanac = input.readlines()

# parse

for line in almanac:

    if line.startswith('seeds:'):
        seedLine = line.split(": ")[1][:-1] #remove newline char
        seeds = list(map(int, seedLine.split(" ")))
        pass



