# https://adventofcode.com/2023/day/3

from enum import Enum

class State(Enum):
    LOOKING_FOR_START_OF_NUMBER = 1
    LOOKING_FOR_END_OF_NUMBER = 2

class PossibleGear:
    def __init__(self, num, location):
        self.num = num
        self.location = location
    def __repr__(self):
        return "Number: " + str(self.num) + "; Location: " + str(self.location)
        

def symbolInRange(schematic, lineNum, charNum):

    symbols = ('*', "#", '/', '$', '=', '%', '@', '+', '&', '-')
    lineOffsets = (-1, 0, 1)
    charOffsets = (-1, 0, 1)
    possibleGear = False
    symbolLocation = [None,None]

    for lineOffset in lineOffsets:
        for charOffset in charOffsets:
            lineToCheck = lineNum+lineOffset
            charToCheck = charNum+charOffset

            if lineToCheck < 0 or lineToCheck >= len(schematic) or charToCheck < 0 or charToCheck > len(schematic[lineToCheck]):
                continue

            if schematic[lineToCheck][charToCheck] in symbols:
                if schematic[lineToCheck][charToCheck] == '*':
                    possibleGear = True
                    symbolLocation = [charToCheck, lineToCheck]
                return (True, possibleGear, symbolLocation)
            
    return (False, possibleGear, symbolLocation)

def isGear(schematic, lineNum, charNum):
    pass



input = open('day3/day3_1.txt', 'r')
schematic = input.readlines()

sumParts = 0
gears = []
gearProduct = 0

for (lineNum, line) in enumerate(schematic):

    state = State.LOOKING_FOR_START_OF_NUMBER
    isPartNumber = False
    isPossibleGear = False
    gearLocation = None


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
                partData = symbolInRange(schematic, lineNum, index)
                if partData[0]:
                    isPartNumber = True
                    isPossibleGear = partData[1]
                    gearLocation = partData[2]

            if not char.isdigit() or index == 0:
                if isPartNumber == True:
                    sumParts += num
                    print(f'num: {num}')   

                if isPossibleGear == True:
                    possibleGear = PossibleGear(num, gearLocation)
                    gears.append(possibleGear)

                num = 0
                exponent = 0
                state = state = State.LOOKING_FOR_START_OF_NUMBER
                isPartNumber = False
                isPossibleGear = False
                gearLocation = None
        index -= 1

print(f'Sum of parts is {sumParts}')

for (id, gear) in enumerate(gears):
    location = gear.location
    for searchGear in gears:
        if searchGear.num == gear.num:
            continue
        if location == searchGear.location:
            print(f'Gear pair: {gear.num}, {searchGear.num}')
            gearProduct += searchGear.num * gear.num
            gears.remove(gear)
            gears.remove(searchGear)

print(f'Product of gears: {gearProduct}')


