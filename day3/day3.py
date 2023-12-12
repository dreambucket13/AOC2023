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

def getGearRatio(numArray, row, column):

    rowOffsets = (-1, 0, 1)
    columnOffsets = (-1, 0, 1)
    gearOne = 0
    gearTwo = 0

    for rowOffset in rowOffsets:
        for columnOffset in columnOffsets:
            rowToCheck = row+rowOffset
            columnToCheck = column+columnOffset

            if rowOffset == 0 and columnOffset == 0:
                continue

            if rowToCheck < 0 or rowToCheck >= len(numArray) or columnToCheck < 0 or columnToCheck > len(numArray[rowToCheck]):
                continue

            if numArray[rowToCheck][columnToCheck] != '0':

                if gearOne == 0:
                    gearOne = int(numArray[rowToCheck][columnToCheck])
                elif gearTwo == 0:
                    gearTwo = int(numArray[rowToCheck][columnToCheck])
            
    return gearOne * gearTwo
    

input = open('day3/day3_1.txt', 'r')
schematic = input.readlines()

rows = len(schematic) 
cols = len(schematic[0]) - 1 # don't count the /n

numArray = [[0 for col in range(cols)] for row in range(rows)]

#numArray is [row][col]


sumParts = 0

for (lineNum, line) in enumerate(schematic):

    state = State.LOOKING_FOR_START_OF_NUMBER
    isPartNumber = False

    index = len(line) - 2 # don't count the /n
    num = 0
    exponent = 0
    numStart = 0
    numEnd = 0

    while index >= 0:
        char = line[index]
        if state == State.LOOKING_FOR_START_OF_NUMBER:
            if char.isdigit():
                state = State.LOOKING_FOR_END_OF_NUMBER
                numStart = index
            # for later gear calc    
            if char == '*':
                numArray[lineNum][index] = '*'

        if state == State.LOOKING_FOR_END_OF_NUMBER:
            if char.isdigit():
                num += (int(char)*pow(10, exponent))
                exponent += 1
                if symbolInRange(schematic, lineNum, index):
                    isPartNumber = True
                numEnd = index

            if not char.isdigit() or index == 0:
                # log the num in a 2D array
                for i in range(numEnd, numStart + 1):
                    numArray[lineNum][i] = num

                if isPartNumber == True:
                    sumParts += num
                    #print(f'num: {num}')
                num = 0
                exponent = 0
                state = state = State.LOOKING_FOR_START_OF_NUMBER
                isPartNumber = False

        index -= 1

print(f'Sum of parts is {sumParts}')

# for j in range(0, rows):
#     print(f'{numArray[j]}, length: {len(numArray[j])}')

gearRatio = 0

for row in range(rows):
    for col in range(cols):
        if numArray[row][col] == '*':
            gearRatio += getGearRatio(numArray, row, col)

print(f'Sum of gear ratios is {gearRatio}')