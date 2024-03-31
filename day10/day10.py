# https://adventofcode.com/2023/day/10

# row, col, name
SOUTH = (1, 0, 'South')
NORTH = (-1, 0, 'North')
EAST = (0, 1, 'East')
WEST = (0, -1, 'West')

ROW = 0
COL = 1
NAME = 2

def findStart(map: list) -> tuple:
    for row, line in enumerate(map):
        for col, char in enumerate(line):
            if char == 'S':
                return (row, col)
            
def exitDirection(currentPosition: tuple, map: list) -> tuple:
    pass

def initialDirections(position: tuple, map: list) -> tuple:
                        
    directionsToCheck = ( NORTH, SOUTH, EAST, WEST )

    validDirections = []

    for directionToCheck in directionsToCheck:

        rowToCheck = position[ROW] + directionToCheck[ROW]
        colToCheck = position[COL] + directionToCheck[COL]

        if 0 > (rowToCheck) or (rowToCheck) >= len(map[0]):
            continue

        if 0 > (colToCheck) or (colToCheck) >= len(map):
            continue

        if directionToCheck[NAME] == 'North':
            #these accept movement from the south
            if map[rowToCheck][colToCheck] in ('|', '7', 'F'):
                validDirections.append( (rowToCheck, colToCheck))

        if directionToCheck[NAME] == 'South':
            #these accept movement from the north
            if map[rowToCheck][colToCheck] in ('|', 'L', 'J'):
                validDirections.append( (rowToCheck, colToCheck))

        if directionToCheck[NAME] == 'East':
            #these accept movement from the west
            if map[rowToCheck][colToCheck] in ('-', '7', 'J'):
                validDirections.append( (rowToCheck, colToCheck))

        if directionToCheck[NAME] == 'West':
            #these accept movement from the east
            if map[rowToCheck][colToCheck] in ('-', 'L', 'F'):
                validDirections.append( (rowToCheck, colToCheck))

    return validDirections


def main():

    map = []

    with open('day10/day10_0.txt') as input:
        inputLines = input.readlines()

    for line in inputLines:
        line = line.replace('\n', '')
        map.append([*line])

    start = findStart(map)

    initial = initialDirections( start , map)

    #expect (2,1) and (3,0)
    print(initial)

    pass

if __name__ == '__main__':
    main()