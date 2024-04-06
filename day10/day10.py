# https://adventofcode.com/2023/day/10

# row, col
SOUTH = (1, 0)
NORTH = (-1, 0)
EAST = (0, 1)
WEST = (0, -1)

ROW = 0
COL = 1

class PositionAndDirection:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


def findStart(map: list) -> tuple:
    for row, line in enumerate(map):
        for col, char in enumerate(line):
            if char == 'S':
                return (row, col)

def movePosition(direction: tuple, position: tuple):

    position = tuple(map(lambda i, j: i + j, position, direction))

    return position

def nextPosition(currentPositionAndDirection: PositionAndDirection, map: list) -> tuple:
    
    currentPosition = currentPositionAndDirection.position
    moveDirection = currentPositionAndDirection.direction

    currentPipe = map[currentPosition[ROW]][currentPosition[COL]]

    newDirection = None
    newPosition = None

    if moveDirection == NORTH:
        match currentPipe:
            case '|':
                newDirection = NORTH
            case '7':
                newDirection = WEST
            case 'F':
                newDirection = EAST
    elif moveDirection == SOUTH:
        match currentPipe:
            case '|':
                newDirection = SOUTH
            case 'L':
                newDirection = EAST
            case 'J':
                newDirection = WEST
    elif moveDirection == EAST:
        match currentPipe:
            case '-':
                newDirection = EAST
            case 'J':
                newDirection = NORTH
            case '7':
                newDirection = SOUTH
    elif moveDirection == WEST:
        match currentPipe:
            case '-':
                newDirection = WEST
            case 'L':
                newDirection = NORTH
            case 'F':
                newDirection = SOUTH

    newPosition = movePosition(newDirection, currentPosition)

    return PositionAndDirection(newPosition, newDirection)

              

def initialDirections(initialPosition: tuple, map: list) -> list:
                        
    directionsToCheck = ( NORTH, SOUTH, EAST, WEST )

    initialPositionsAndDirections = []

    for directionToCheck in directionsToCheck:

        rowToCheck = initialPosition[ROW] + directionToCheck[ROW]
        colToCheck = initialPosition[COL] + directionToCheck[COL]

        if 0 > (rowToCheck) or (rowToCheck) >= len(map[0]):
            continue

        if 0 > (colToCheck) or (colToCheck) >= len(map):
            continue

        if directionToCheck == NORTH:
            #these accept movement from the south
            if map[rowToCheck][colToCheck] in ('|', '7', 'F'):
                initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), NORTH) )

        elif directionToCheck == SOUTH:
            #these accept movement from the north
            if map[rowToCheck][colToCheck] in ('|', 'L', 'J'):
                initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), SOUTH) )

        elif directionToCheck == EAST:
            #these accept movement from the west
            if map[rowToCheck][colToCheck] in ('-', '7', 'J'):
                initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), EAST) )

        elif directionToCheck == WEST:
            #these accept movement from the east
            if map[rowToCheck][colToCheck] in ('-', 'L', 'F'):
                initialPositionsAndDirections.append(  PositionAndDirection((rowToCheck, colToCheck), WEST))

    return initialPositionsAndDirections

def storePipeLocations(location: tuple, pipeLocations: dict):
    
    row = location[ROW]
    col = location[COL]

    if row not in pipeLocations:
        pipeLocations[row] = [col]
    else:
        pipeLocations[row].append(col)
    
    return pipeLocations
    

def main():

    map = []
    pipeLocations = {}

    with open('day10/day10_1.txt') as input:
        inputLines = input.readlines()

    for line in inputLines:
        line = line.replace('\n', '')
        map.append([*line])

    start = findStart(map)

    pipeLocations = storePipeLocations(start, pipeLocations)

    way1, way2 = initialDirections(start , map)

    for way in way1, way2:
        pipeLocations = storePipeLocations(way.position, pipeLocations)

    steps = 1

    while way1.position != way2.position:
        
        # print(f'way 1: {way1}, way 2: {way2}')
        way1 = nextPosition(way1, map)
        way2 = nextPosition(way2, map)
        for way in way1, way2:
            pipeLocations = storePipeLocations(way.position, pipeLocations)
        steps += 1

    print(f'steps: {steps}')

    #part 2



if __name__ == '__main__':
    main()