import re

input = open('test.txt', 'r')
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

calibration = 0

for line in lines:
    first = 0
    last = 0
    min_index = 10000
    max_index = 0

    for (index, regex) in enumerate(regexes):
        for x in regex:
            match = x.search(line)
            if match == None:
                continue
            print(match.span())
            if match.span()[0] < min_index:
                min_index = match.span()[0]
                first = index + 1
            if match.span()[0] > max_index:
                max_index = match.span()[0]
                last = index + 1
    calibration += first*10 + last

    print(f"line cal: {first*10 + last} for line: {line}")

print(f"calibration is {calibration}")


        