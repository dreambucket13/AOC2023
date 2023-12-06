# https://adventofcode.com/2023/day/1

import re

input = open('day1_2.txt', 'r')
lines = input.readlines()

calibration = 0

one = re.compile(r'one|1')
two = re.compile(r'two|2')
three = re.compile(r'three|3')
four = re.compile(r'four|4')
five = re.compile(r'five|5')
six = re.compile(r'six|6')
seven = re.compile(r'seven|7')
eight = re.compile(r'eight|8')
nine = re.compile(r'nine|9')

regexes = [ one, 
            two,
            three, 
            four, 
            five,
            six, 
            seven, 
            eight, 
            nine ]

calibration = 0

for line in lines:
    first = 0
    last = 0

    #from start
    line_index = 1
    match = None
    while match == None:
        for (regex_num, regex) in enumerate(regexes):
            match = regex.search(line[:line_index])
            if match != None:
                first = regex_num + 1
                break
        if match == None:
            line_index += 1

    #from end
    line_index = len(line) 
    match = None
    while match == None:
        for (regex_num, regex) in enumerate(regexes):
            match = regex.search(line[line_index:])
            if match != None:
                last = regex_num + 1
                break
        if match == None:
            line_index -= 1


    calibration += first*10 + last

    print(f"line cal: {first*10 + last} for line: {line}")

print(f"calibration is {calibration}")


        