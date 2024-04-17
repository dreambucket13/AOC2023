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
            elif partOfMainLoop( (rowIndex, colIndex), pipeLocations):
                print("\033[92m{}\033[00m".format(col), end = '')
            else:
                print(col, end = '')
        print('')


def main():

    map = []
    pipeLocations = {}


    with open('day10/day10_0b.txt') as input:
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

    #initial interior vector is the direction of the 1st turn
    print("loop 1 ----------------")
    interiorVector = None
    for position in pipeLoop1:
        if map[position.position[ROW]][position.position[COL]] in ('L', '7', 'F', 'J'):
            interiorVector = position.exitDirection
            break
    for position in pipeLoop1:

        #update vector
        interiorVector = setInteriorVector(position, interiorVector, map)
        position.interiorVector = interiorVector
        #fire ray trace in interior direction
        interiorTiles = traceRay(position.position, interiorVector, pipeLocations, interiorTiles, map)

        printInteriorVectors(interiorTiles, pipeLocations, map, pipeLoop1, pipeLoop2)
        pass
        # print(f'position: {position.position}, pipe: {map[position.position[ROW]][position.position[COL]]} interior: {vectorToText(interiorVector)} approach: {vectorToText(position.approachDirection)} exit: {vectorToText(position.exitDirection)}')

    print("loop 2 ----------------")
    interiorVector = None
    for position in pipeLoop2:
        if map[position.position[ROW]][position.position[COL]] in ('L', '7', 'F', 'J'):
            interiorVector = position.exitDirection
            break

    for position in pipeLoop2:

        #update vector
        interiorVector = setInteriorVector(position, interiorVector, map)
        position.interiorVector = interiorVector
        #fire ray trace in interior direction
        interiorTiles = traceRay(position.position, interiorVector, pipeLocations, interiorTiles, map)
        printInteriorVectors(interiorTiles, pipeLocations, map, pipeLoop1, pipeLoop2)
        pass
        # print(f'position: {position.position}, pipe: {map[position.position[ROW]][position.position[COL]]} interior: {vectorToText(interiorVector)} approach: {vectorToText(position.approachDirection)} exit: {vectorToText(position.exitDirection)}')        


    #3172 is too high
    print(f'num interior tiles: {len(interiorTiles)}')
    # printInternalTiles(interiorTiles, pipeLocations, map)
    printInteriorVectors(interiorTiles, pipeLocations, map, pipeLoop1, pipeLoop2)
if __name__ == '__main__':
    main()