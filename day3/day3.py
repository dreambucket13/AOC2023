# https://adventofcode.com/2023/day/3

from enum import Enum

class State(Enum):
    LOOKING_FOR_START_OF_NUMBER = 1
    LOOKING_FOR_END_OF_NUMBER = 2

def symbolInRange(schematic, lineNum, charNum):

    symbols = ('*', "#", '/', '$', '=', '%', '@', '+', '&', '-')
    lineOffsets = (-1, 0, 1)
    charOffsets = (-1, 0, 1)

    for lineOffset in lineOffsets:
        for charOffset in charOffsets:
            lineToCheck = lineNum+lineOffset
            charToCheck = charNum+charOffset

            if lineToCheck < 0 or lineToCheck >= len(schematic) or charToCheck < 0 or charToCheck > len(schematic[lineToCheck]):
                continue

            if schematic[lineToCheck][charToCheck] in symbols:
                return True
            
    return False

def isGear(schematic, lineNum, charNum):
    pass



input = open('day3/day3_1.txt', 'r')
schematic = input.readlines()

sumParts = 0

for (lineNum, line) in enumerate(schematic):

    state = State.LOOKING_FOR_START_OF_NUMBER
    isPartNumber = False

    index = len(line) - 2
    num = 0
    exponent = 0

    while index >= 0:
        char = line[index]
        if state == State.LOOKING_FOR_START_OF_NUMBER:
            if char.isdigit():
                state = State.LOOKING_FOR_END_OF_NUMBER

        if state == State.LOOKING_FOR_END_OF_NUMBER:
            if char.isdigit():
                num += (int(char)*pow(10, exponent))
                exponent += 1
                if symbolInRange(schematic, lineNum, index):
                    isPartNumber = True

            if not char.isdigit() or index == 0:
                if isPartNumber == True:
                    sumParts += num
                    print(f'num: {num}')
                num = 0
                exponent = 0
                state = state = State.LOOKING_FOR_START_OF_NUMBER
                isPartNumber = False

        index -= 1

print(f'Sum of parts is {sumParts}')