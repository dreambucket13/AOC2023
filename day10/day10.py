# https://adventofcode.com/2023/day/10

# row, col
SOUTH = (1, 0)
NORTH = (-1, 0)
EAST = (0, 1)
WEST = (0, -1)

NORTH_EAST = (-1, 1)
NORTH_WEST = (-1, -1)
SOUTH_EAST = (1, 1)
SOUTH_WEST = (1, -1)

#in order clockwise
DIRECTIONS = (NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST)

ROW = 0
COL = 1

class PositionAndDirection:
    def __init__(self, position, approachDirection, exitDirection, interiorVector = None):
        self.position = position
        self.approachDirection = approachDirection
        self.exitDirection = exitDirection
        self.interiorVector = interiorVector

def swapExitAndApproach(exitDirection):

    if exitDirection == EAST:
        return WEST
    elif exitDirection == WEST:
        return EAST
    elif exitDirection == SOUTH:
        return NORTH   
    elif exitDirection == NORTH:
        return SOUTH 
    else:
        return None

def nextPosition(currentPositionAndDirection: PositionAndDirection, map: list) -> tuple:
    
    currentPosition = currentPositionAndDirection.position
    exitDirection = currentPositionAndDirection.exitDirection


    newPosition = movePosition(exitDirection, currentPosition)

    nextPipe = map[newPosition[ROW]][newPosition[COL]]
    nextApproachDirection = swapExitAndApproach(exitDirection)
    nextExitDirection = None

    if nextApproachDirection == SOUTH:
        match nextPipe:
            case '|':
                nextExitDirection = NORTH
            case '7':
                nextExitDirection = WEST
            case 'F':
                nextExitDirection = EAST
    elif nextApproachDirection == NORTH:
        match nextPipe:
            case '|':
                nextExitDirection = SOUTH
            case 'L':
                nextExitDirection = EAST
            case 'J':
                nextExitDirection = WEST
    elif nextApproachDirection == WEST:
        match nextPipe:
            case '-':
                nextExitDirection = EAST
            case 'J':
                nextExitDirection = NORTH
            case '7':
                nextExitDirection = SOUTH
    elif nextApproachDirection == EAST:
        match nextPipe:
            case '-':
                nextExitDirection = WEST
            case 'L':
                nextExitDirection = NORTH
            case 'F':
                nextExitDirection = SOUTH

    return PositionAndDirection(newPosition, swapExitAndApproach(nextApproachDirection), nextExitDirection)

def findStart(map: list) -> tuple:
    for row, line in enumerate(map):
        for col, char in enumerate(line):
            if char == 'S':
                return (row, col)

def movePosition(direction: tuple, position: tuple):

    position = tuple(map(lambda i, j: i + j, position, direction))

    return position

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
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), SOUTH, NORTH) )
                case '7':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), SOUTH, WEST) )
                case 'F':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), SOUTH, EAST) )
        elif directionToCheck == SOUTH:
            #these accept movement from the north
            # if map[rowToCheck][colToCheck] in ('|', 'L', 'J'):
            match pipeType:
                case '|':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), NORTH, SOUTH) )
                case 'L':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), NORTH, EAST) )
                case 'J':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), NORTH, WEST) )

        elif directionToCheck == EAST:
            #these accept movement from the west
            # if map[rowToCheck][colToCheck] in ('-', '7', 'J'):
            match pipeType:
                case '-':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), WEST, EAST) )
                case '7':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), WEST, SOUTH) )
                case 'J':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), WEST, NORTH) )

        elif directionToCheck == WEST:
            #these accept movement from the east
            # if map[rowToCheck][colToCheck] in ('-', 'L', 'F'):
            match pipeType:
                case '-':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), EAST, WEST) )
                case 'L':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), EAST, NORTH) )
                case 'F':
                    initialPositionsAndDirections.append( PositionAndDirection((rowToCheck, colToCheck), EAST, SOUTH) )

    return initialPositionsAndDirections

def storePipeLocationsDict(location: tuple, pipeLocations: dict, map):
    
    row = location[ROW]
    col = location[COL]
    pipe = map[ROW][COL]

    if (row,col) not in pipeLocations:
        pipeLocations[(row,col)] = pipe
    
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

def vectorToText(vector):
    if vector == NORTH:
        return "North"
    elif vector == SOUTH:
        return "South"
    elif vector == EAST:
        return "East"
    elif vector == WEST:
        return "West"
    elif vector == NORTH_WEST:
        return "North West"
    elif vector == NORTH_EAST:
        return "North East"
    elif vector == SOUTH_WEST:
        return "South West"    
    elif vector == SOUTH_EAST:
        return "South East"

def printInternalTiles(interiorTiles, pipeLocations, map):

    for rowIndex, row in enumerate(map):
        for colIndex, col in enumerate(row):
            if (rowIndex,colIndex) in interiorTiles:
                print("\033[91m{}\033[00m".format(col), end = '')
            elif (rowIndex, colIndex) in pipeLocations:
                print("\033[92m{}\033[00m".format(col), end = '')
            else:
                print(col, end = '')
        print('')

def replaceSwithPipe(map, start, initialDirections):

    exitDirectionsFromS = (swapExitAndApproach(initialDirections[0].approachDirection), swapExitAndApproach(initialDirections[1].approachDirection))

    if exitDirectionsFromS == (EAST, WEST) or exitDirectionsFromS == (WEST, EAST):
        map[start[ROW]][start[COL]] = '-'

    if exitDirectionsFromS == (NORTH, SOUTH) or exitDirectionsFromS == (SOUTH, NORTH):
        map[start[ROW]][start[COL]] = '|'

    if exitDirectionsFromS == (SOUTH, EAST):
        map[start[ROW]][start[COL]] = 'F'

    if exitDirectionsFromS == (NORTH, WEST):
        map[start[ROW]][start[COL]] = '7'

    if exitDirectionsFromS == (NORTH, EAST):
        map[start[ROW]][start[COL]] = 'L'

    if exitDirectionsFromS == (NORTH, WEST):
        map[start[ROW]][start[COL]] = 'J'

    return map


def analyzeMaze(file):

    map = []
    pipeLocations = {}


    with open(file) as input:
        inputLines = input.readlines()

    for line in inputLines:
        line = line.replace('\n', '')
        map.append([*line])

    start = findStart(map)

    pipeLoop1 = []
    pipeLoop2 = []
    

    pipeLocations = storePipeLocationsDict(start, pipeLocations, map)

    way1, way2 = initialDirections(start , map)

    pipeLoop1.append(PositionAndDirection(start,None,way1))
    pipeLoop2.append(PositionAndDirection(start,None,way2))
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

    interiorTiles = []

    way1, way2 = initialDirections(start , map)
    map = replaceSwithPipe(map, start, (way1, way2))

    for rowIndex, row in enumerate(map):
        
        inLoop = False
        lastTurn = None

        for colIndex, pipe in enumerate(row):
    
            if (rowIndex, colIndex) in pipeLocations:
                if pipe in ('|'):
                    inLoop = not inLoop

                if pipe in ('7'):
                    # if last turn was F, that's a U turn, don't toggle the in loop state.
                    if lastTurn != 'F':
                        inLoop = not inLoop

                if pipe in ('J'):
                    # if last turn was L, that's a U turn, don't toggle the in loop state.
                    if lastTurn != 'L':
                        inLoop = not inLoop
                
                if pipe not in ('-', '|'):
                    lastTurn = pipe

            if inLoop and (rowIndex, colIndex) not in pipeLocations:
                interiorTiles.append((rowIndex, colIndex))
  
    # printInternalTiles(interiorTiles, pipeLocations, map)
    print(f'Internal tiles: {len(interiorTiles)}')
    return len(interiorTiles)

if __name__ == '__main__':
    assert analyzeMaze('day10/day10_0a.txt') == 4
    assert analyzeMaze('day10/day10_0b.txt') == 4
    assert analyzeMaze('day10/day10_0c.txt') == 8
    assert analyzeMaze('day10/day10_0d.txt') == 10
    assert analyzeMaze('day10/day10_1.txt') == 601

    assert analyzeMaze('day10/day10_steves.txt') == 305

    assert analyzeMaze('day10/day10_0e.txt') == 9
