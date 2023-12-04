import re

input = open('day1_1.txt', 'r')
lines = input.readlines()

calibration = 0

one = re.compile(r'one')
two = re.compile(r'two')
three = re.compile(r'three')
four = re.compile(r'four')
five = re.compile(r'five')
six = re.compile(r'six')
seven = re.compile(r'seven')
eight = re.compile(r'eight')
nine = re.compile(r'nine')

one_digit = re.compile(r'1')
two_digit = re.compile(r'2')
three_digit = re.compile(r'3')
four_digit = re.compile(r'4')
five_digit = re.compile(r'5')
six_digit = re.compile(r'6')
seven_digit = re.compile(r'7')
eight_digit = re.compile(r'8')
nine_digit = re.compile(r'9')

regexes = [ [one, one_digit], 
            [two, two_digit],
            [three, three_digit],
            [four, four_digit], 
            [five, five_digit],
            [six, six_digit],
            [seven, seven_digit],
            [eight, eight_digit],
            [nine, nine_digit] ]

first = 0
last = 0

for line in lines:
    for (index, regex) in enumerate(regexes):
        for x in regex:
            start = 0
            match =  x.match(line)


        