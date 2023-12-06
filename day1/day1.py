def charToInt(x):
    if x == '1':
        return 1
    elif x == '2':
        return 2
    elif x == '3':
        return 3
    elif x == '4':
        return 4
    elif x == '5':
        return 5
    elif x == '6':
        return 6
    elif x == '7':
        return 7
    elif x == '8':
        return 8
    elif x == '9':
        return 9
    elif x == '0':
        return 0
    else:
        return -1

input = open('day1_1.txt', 'r')
lines = input.readlines()

calibration = 0

for line in lines:
    first = ''
    last = ''
    for char in line:
        if char.isdigit():
            if first == '':
                first = char
                last = char
            else:
                last = char

    increment = charToInt(first)*10 + charToInt(last)
    calibration = calibration + increment

print(f'calibration value is {calibration}')



        



