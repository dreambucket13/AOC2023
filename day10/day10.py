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

def movePosition(direction: tuple, position: tuple):

    position = tuple(map(lambda i, j: i + j, position, direction))

    return position

def nextPosition(currentPosition: tuple, moveDirection, map: list) -> tuple:
    
    currentPipe = map[currentPosition[ROW]][currentPosition[COL]]

    newDirection = None
    newPosition = None

    match moveDirection:
        case 'North':
            match currentPipe:
                case '|':
                    newPosition = movePosition(NORTH, currentPosition)
                    newDirection = 'North'
                case '7':
                    newPosition = movePosition(WEST, currentPosition)
                    newDirection = 'West'
                case 'F':
                    newPosition = movePosition(EAST, currentPosition)
                    newDirection = 'East'
        case 'South':
            match currentPipe:
                case '|':
                    newPosition = movePosition(SOUTH, currentPosition)
                    newDirection = 'South'
                case 'L':
                    newPosition = movePosition(EAST, currentPosition)
                    newDirection = 'East'
                case 'J':
                    newPosition = movePosition(WEST, currentPosition)
                    newDirection = 'West'
        case 'East':
            match currentPipe:
                case '-':
                    newPosition = movePosition(EAST, currentPosition)
                    newDirection = 'East'
                case 'J':
                    newPosition = movePosition(NORTH, currentPosition)
                    newDirection = 'North'
                case '7':
                    newPosition = movePosition(SOUTH, currentPosition)
                    newDirection = 'South'
        case 'West':
            match currentPipe:
                case '-':
                    newPosition = movePosition(WEST, currentPosition)
                    newDirection = 'West'
                case 'L':
                    newPosition = movePosition(NORTH, currentPosition)
                    newDirection = 'North'
                case 'F':
                    newPosition = movePosition(SOUTH, currentPosition)
                    newDirection = 'South'

    return (newPosition, newDirection)

              

def initialDirections(position: tuple, map: list) -> list:
                        
    directionsToCheck = ( NORTH, SOUTH, EAST, WEST )

    initialPositionsAndDirections = []

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
                initialPositionsAndDirections.append( ((rowToCheck, colToCheck), 'North'))

        elif directionToCheck[NAME] == 'South':
            #these accept movement from the north
            if map[rowToCheck][colToCheck] in ('|', 'L', 'J'):
                initialPositionsAndDirections.append( ((rowToCheck, colToCheck), 'South'))

        elif directionToCheck[NAME] == 'East':
            #these accept movement from the west
            if map[rowToCheck][colToCheck] in ('-', '7', 'J'):
                initialPositionsAndDirections.append( ((rowToCheck, colToCheck), 'East'))

        elif directionToCheck[NAME] == 'West':
            #these accept movement from the east
            if map[rowToCheck][colToCheck] in ('-', 'L', 'F'):
                initialPositionsAndDirections.append( ((rowToCheck, colToCheck), 'West'))

    return initialPositionsAndDirections


def main():

    map = []

    with open('day10/day10_1.txt') as input:
        inputLines = input.readlines()

    for line in inputLines:
        line = line.replace('\n', '')
        map.append([*line])

    start = findStart(map)

    initial = initialDirections( start , map)


    way1 = initial[0]

    way2 = initial[1]

    steps = 1

    while way1[0] != way2[0]:
        
        # print(f'way 1: {way1}, way 2: {way2}')
        way1 = nextPosition(way1[0], way1[1], map)
        way2 = nextPosition(way2[0], way2[1], map)
        steps += 1

    print(f'steps: {steps}')

if __name__ == '__main__':
    main()