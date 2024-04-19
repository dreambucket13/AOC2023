# https://adventofcode.com/2023/day/11

def part1(file):

    with open(file) as input:
        inputLines = input.readlines()

    galaxies = []
    rowsToExpand = []
    colsToExpand = [x for x in range(0,len(inputLines[0])-1)]

    for row, line in enumerate(inputLines):
        expandRow = True
        for col, character in enumerate(line):
            if character == '#':
                galaxies.append( [row, col] )
                expandRow = False
                
                if col in colsToExpand:
                    colsToExpand.remove(col)

        if expandRow == True:
            rowsToExpand.append(row)

   
    # assert rowsToExpand == [3, 7]
    # assert colsToExpand == [2,5,8]

    #expand the galaxies.  rows shift galaxies after them to the right.
    # cols shift galaxies below them down (i.e., increase their row num)

    for galaxy in galaxies:
        colExpansion = 0
        rowExpansion = 0

        for col in colsToExpand:

            galaxyX = galaxy[1]
            if galaxyX > col:
                colExpansion += 1

        galaxy[1] += colExpansion

        for row in rowsToExpand:
            galaxyY = galaxy[0]
            if galaxyY > row:
                rowExpansion += 1

        galaxy[0] += rowExpansion


    with open('day11/day11_0_expanded.txt') as expandedTestFile:
        expandedTest = expandedTestFile.readlines()

    testExpandedGalaxies = []
    for row, line in enumerate(expandedTest):
        for col, character in enumerate(line):
            if character == '#':
                testExpandedGalaxies.append( [row, col] )

    # assert galaxies == testExpandedGalaxies
        
    # distance = x delta + y delta

    totalDistance = 0
    checked = {}

    # convert galaxies to tuples so I can hash them.

    galaxies = list(map(tuple, galaxies))

    for galaxy1 in galaxies:
        for galaxy2 in galaxies:

            if galaxy1 == galaxy2 or (galaxy1, galaxy2) in checked:
                continue
            
            totalDistance += abs(galaxy2[0]-galaxy1[0]) + abs(galaxy2[1]-galaxy1[1])

            checked[(galaxy1, galaxy2)] = True
            checked[(galaxy2, galaxy1)] = True
            
    print(totalDistance)
    return totalDistance

if __name__ == '__main__':
    assert part1('day11\day11_0.txt') == 374
    assert part1('day11\day11_1.txt') == 9214785