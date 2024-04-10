# https://adventofcode.com/2023/day/10

# row, col
SOUTH = (1, 0)
NORTH = (-1, 0)
EAST = (0, 1)
WEST = (0, -1)

ROW = 0
COL = 1

class PositionAndDirection:
    def __init__(self, position, approachDirection, exitDirection):
        self.position = position
        self.approachDirection = approachDirection
        self.exitDirection = exitDirection



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
    moveDirection = currentPositionAndDirection.exitDirection

    newDirection = None
    newPosition = movePosition(moveDirection, currentPosition)

    nextPipe = map[newPosition[ROW]][newPosition[COL]]

    if moveDirection == NORTH:
        match nextPipe:
            case '|':
                newDirection = NORTH
            case '7':
                newDirection = WEST
            case 'F':
                newDirection = EAST
    elif moveDirection == SOUTH:
        match nextPipe:
            case '|':
                newDirection = SOUTH
            case 'L':
                newDirection = EAST
            case 'J':
                newDirection = WEST
    elif moveDirection == EAST:
        match nextPipe:
            case '-':
                newDirection = EAST
            case 'J':
                newDirection = NORTH
            case '7':
                newDirection = SOUTH
    elif moveDirection == WEST:
        match nextPipe:
            case '-':
                newDirection = WEST
            case 'L':
                newDirection = NORTH
            case 'F':
                newDirection = SOUTH

    return PositionAndDirection(newPosition, moveDirection, newDirection)

              

def initialDirections(initialPosition: tuple, map: list) -> list:
                        
    directionsToCheck = ( NORTH, SOUTH, EAST, WEST )

    initialPositionsAndDirections = []

    for directionToCheck in directionsToCheck:

        rowToCheck = initialPosition[ROW] + directionToCheck[ROW]
        colToCheck = initialPosition[COL] + directionToCheck[COL]
        pipeType = map[rowToCheck][colToCheck]

        if 0 > (rowToCheck) or (rowToCheck) >= len(map):
            continue

        if 0 > (colToCheck) or (colToCheck) >= len(map[0]):
            continue

        if directionToCheck == NORTH:
            #these accept movement from the south
            # if map[rowToCheck][colToCheck] in ('|', '7', 'F'):
            match pipeType:
                case '|':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), NORTH, SOUTH) )
                case '7':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), NORTH, WEST) )
                case 'F':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), NORTH, EAST) )
        elif directionToCheck == SOUTH:
            #these accept movement from the north
            # if map[rowToCheck][colToCheck] in ('|', 'L', 'J'):
            match pipeType:
                case '|':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), SOUTH, SOUTH) )
                case 'L':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), SOUTH, EAST) )
                case 'J':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), SOUTH, WEST) )

        elif directionToCheck == EAST:
            #these accept movement from the west
            # if map[rowToCheck][colToCheck] in ('-', '7', 'J'):
            match pipeType:
                case '-':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), EAST, EAST) )
                case '7':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), EAST, SOUTH) )
                case 'J':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), EAST, NORTH) )

        elif directionToCheck == WEST:
            #these accept movement from the east
            # if map[rowToCheck][colToCheck] in ('-', 'L', 'F'):
            match pipeType:
                case '-':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), WEST, WEST) )
                case 'L':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), WEST, NORTH) )
                case 'F':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), WEST, SOUTH) )

    return initialPositionsAndDirections

def storePipeLocationsDict(location: tuple, pipeLocations: dict, map):
    
    row = location[ROW]
    col = location[COL]

    if row not in pipeLocations:
        pipeLocations[row] = [col]
    elif col not in pipeLocations[row]:
        pipeLocations[row].append(col)
    
    return pipeLocations


def partOfMainLoop(location, pipeLocations):
    row = location[ROW]
    col = location[COL]

    if row not in pipeLocations:
        return False
    elif col not in pipeLocations[row]:
        return False
    else:
        return True

def rotateCounterClockWise(vector):
    if vector == NORTH:
        return WEST
    elif vector == EAST:
        return NORTH
    elif vector == WEST:
        return SOUTH
    elif vector == SOUTH:
        return EAST

def rotateClockWise(vector):
    if vector == NORTH:
        return EAST
    elif vector == EAST:
        return SOUTH
    elif vector == WEST:
        return NORTH
    elif vector == SOUTH:
        return WEST


def setInteriorVector(positionAndDirection, currentInteriorVector, map):
    
    position =  positionAndDirection.position
    direction = positionAndDirection.approachDirection

    pipeType = map[position[ROW]][position[COL]]

    interiorVector = currentInteriorVector

    if direction == SOUTH:
        match pipeType:
            case 'J':
                interiorVector = rotateClockWise(interiorVector)
            case 'L':
                interiorVector = rotateCounterClockWise(interiorVector)
    elif direction == WEST:
         match pipeType :
            case 'L':
                interiorVector = rotateClockWise(interiorVector)   
            case 'F':
                interiorVector = rotateCounterClockWise(interiorVector)   
    elif direction == EAST:
         match pipeType :
            case '7':
                interiorVector = rotateClockWise(interiorVector)   
            case 'J':
                interiorVector = rotateCounterClockWise(interiorVector) 
    elif direction == NORTH:
         match pipeType :
            case 'F':
                interiorVector = rotateClockWise(interiorVector)   
            case '7':
                interiorVector = rotateCounterClockWise(interiorVector) 

    return interiorVector

def traceRay(location, interiorVector, pipeLocations, interiorTiles):

    trace = movePosition(interiorVector, location)

    while partOfMainLoop(trace, pipeLocations) == False:
        trace = movePosition(interiorVector, trace)
        
        if trace not in interiorTiles:
            interiorTiles.append(trace)
    
    return interiorTiles


def main():

    map = []
    pipeLocations = {}


    with open('day10/day10_1.txt') as input:
        inputLines = input.readlines()

    for line in inputLines:
        line = line.replace('\n', '')
        map.append([*line])

    start = findStart(map)

    pipeLoop1 = [start]
    pipeLoop2 = [start]


    pipeLocations = storePipeLocationsDict(start, pipeLocations, map)

    way1, way2 = initialDirections(start , map)

    pipeLoop1.append(way1)
    pipeLoop2.append(way2)

    for way in way1, way2:
        pipeLocations = storePipeLocationsDict(way.position, pipeLocations, map)

    steps = 1

    while way1.position != way2.position:
        
        # print(f'way 1: {way1}, way 2: {way2}')
        way1 = nextPosition(way1, map)
        way2 = nextPosition(way2, map)
        for way in way1, way2:
            pipeLocations = storePipeLocationsDict(way.position, pipeLocations, map)

        pipeLoop1.append(way1)
        pipeLoop2.append(way2)
        
        steps += 1

    print(f'steps: {steps}')

    #part 2

    tilesInLoop = 0
    totalArea = 0

    for position in reversed(pipeLoop2):
        if position in pipeLoop1:
            continue
        pipeLoop1.append(position)

    #initial interior vector is the direction of the 1st turn
    interiorVector = None
    priorDirection = pipeLoop1[1].approachDirection
    for position in pipeLoop1[1:]:
        if position.approachDirection != position.exitDirection:
            interiorVector = position.exitDirection
            break



    interiorTiles = []


    for position in pipeLoop1[1:]:

        #update vector
        interiorVector = setInteriorVector(position, interiorVector, map)
        #fire ray trace in interior direction
        interiorTiles = traceRay(position.position, interiorVector, pipeLocations, interiorTiles)

        print(f'position: {position.position}, pipe: {map[position.position[ROW]][position.position[COL]]} interiorVector: {interiorVector}')
        pass

    print(f'tiles in loop: {totalArea - steps*2}')
        


if __name__ == '__main__':
    main()