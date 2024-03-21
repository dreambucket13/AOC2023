# https://adventofcode.com/2023/day/5

def getMap(mapName: str, almanac: list, lineNum: int):

    if almanac[lineNum].startswith(mapName):

        mapLineNum = lineNum + 1
        mapLine = almanac[mapLineNum]

        conversionMap = []

        while not mapLine.startswith('\n'):

            if mapLine[-1] == '\n':
                mapLine = mapLine[:-1]

            mapIntegers = list(map(int, mapLine.split(" ")))

            #do the range stuff here
            mapRange = mapIntegers[2] - 1
            distinationStart = mapIntegers[0]
            sourceStart = mapIntegers[1]

            parsedMap = {}

            parsedMap['Destination'] = (distinationStart, distinationStart + mapRange)
            parsedMap['Source'] = (sourceStart, sourceStart + mapRange)

            conversionMap.append(parsedMap)

            if mapLineNum + 1 < len(almanac):
                mapLineNum += 1
                mapLine = almanac[mapLineNum]
            else:
                break

        return conversionMap
    else:
        return None

def mapSeed(seed: int, parsedMaps: dict) -> int:
    
    location = seed

    START = 0
    END = 1
    
    for currentMap in parsedMaps:
        for line in parsedMaps[currentMap]:
            source = line['Source']
            destination = line['Destination']

            if source[START] <= location <= source[END]:
                location = destination[START] + (location - source[START])
                break
        
    return location

def mapSeedVerbose(seed: int, parsedMaps: dict) -> int:
    
    location = seed

    START = 0
    END = 1
    
    priorLocation = location

    for currentMap in parsedMaps:
        for line in parsedMaps[currentMap]:
            source = line['Source']
            destination = line['Destination']

            if source[START] <= location <= source[END]:
                location = destination[START] + (location - source[START])
                break

        if location < priorLocation:
            print(f'Moved up to {location}')
        elif location > priorLocation:
            print(f"Moved down to {location}")
        else:
            print(f'Stayed the same at {location}')

        priorLocation = location

    return location


def mapSeedReverse(locationToBackTrack: int, parsedMaps: dict) -> int:
    
    location = locationToBackTrack

    START = 0
    END = 1
    
    #destination and source are swapped since I am going the other way
    for currentMap in reversed(parsedMaps):
        for line in parsedMaps[currentMap]:
            source = line['Destination']
            destination = line['Source']

            if source[START] <= location <= source[END]:
                location = destination[START] + (location - source[START])
                break
        
    return location

def isValidSeed(seedToFind: int, seeds:tuple):

    for (index, seed) in enumerate(seeds):
        if index % 2 == 0:
            rangeStart = seeds[index]
            rangeLength = seeds[index + 1]
            rangeEnd = rangeStart + rangeLength
            if rangeStart <= seedToFind <= rangeEnd:
                return True
        else:
            continue
    return False

def morphRange(seedRange: tuple, sourceRange, destinationRange) -> tuple:

    remainderBefore = None
    remainderAfter = None
    morphed = seedRange
    matched = False

    ranges = (remainderBefore, morphed, remainderAfter), matched

    # no overlap
    if seedRange[1] < sourceRange[0] or seedRange[0] > sourceRange[1]:
        return ranges
    
    matched = True

    delta = destinationRange[0] - sourceRange[0]

    intersectionStart = 0
    intersectionEnd = 0

    # the larger one is the intersection start
    if seedRange[0] > sourceRange[0]:
        intersectionStart = seedRange[0]
    else:
        intersectionStart = sourceRange[0]

    # the smaller one is the intersection end
    if seedRange[1] < sourceRange[1]:
        intersectionEnd = seedRange[1]
    else:
        intersectionEnd = sourceRange[1]

    intersection = intersectionStart, intersectionEnd
    morphed = (intersectionStart + delta, intersectionEnd + delta)

    #need a reminder before?
    if seedRange[0] < sourceRange[0]:
        remainderBefore = seedRange[0], sourceRange[0] - 1

    #need a reminder after?
    if seedRange[1] > sourceRange[1]:
        remainderAfter = sourceRange[1] + 1, seedRange[1]

    ranges = (remainderBefore, morphed, remainderAfter), matched
    return ranges

def main():
    fileName = 'day5/day5_0.txt'
    input = open(fileName, 'r')
    almanac = input.readlines()

    mapTypes = ('seed-to-soil map:',
                'soil-to-fertilizer map:',
                'fertilizer-to-water map:',
                'water-to-light map:',
                'light-to-temperature map:',
                'temperature-to-humidity map:',
                'humidity-to-location map:')

    # parse

    parsedMaps = {}
    for (lineNum, line) in enumerate(almanac):

        if line.startswith('seeds:'):
            seedLine = line.split(": ")[1][:-1] #remove newline char
            seeds = list(map(int, seedLine.split(" ")))
            continue

        for mapType in mapTypes:
            parsedMap = getMap(mapType, almanac, lineNum)
            if parsedMap != None:
                parsedMaps[mapType] = parsedMap

    print('Maps parsed')
    # map the seeds for part 1
    lowestLocation = None
    for seed in seeds:

        location = mapSeed(seed, parsedMaps)

        if lowestLocation == None or location < lowestLocation:
            lowestLocation = location

    print(f'Part 1 lowest location: {lowestLocation}')

    #part 2 try 2

    seedRanges = []

    for index, seed in enumerate(seeds):
        if index % 2 != 0:
            continue
        seedRanges.append((seed, seed + seeds[index + 1] - 1))

    #first map the seeds brute force
    # for seedRange in seedRanges:
    #     for seed in range(seedRange[0], seedRange[1] + 1):
    #         print(f'start: {seed}, mapped: {mapSeed(seed, parsedMaps)}')


    test1 = morphRange((0,1), (10,20), (110,130))
    print(test1)
    test2 = morphRange((15,18), (10,20), (110,120))
    print(test2)
    print(morphRange((15,22), (10,20), (110,120)))
    print(morphRange((5,25), (10,20), (110,120)))
    print(morphRange((9,21), (10,20), (110,120)))
    # for mapType in mapTypes:
    #     pendingSeedRanges = []
    #     for seedRange in seedRanges:
    #         for mapLine in parsedMaps[mapType]:
    #             matchInfo = morphRange(seedRange, mapLine['Source'], mapLine['Destination'])
    #             morphedRanges = matchInfo[0]
    #             matched = matchInfo[1]

    #             if matched == True:
    #                 for morphedRange in morphedRanges:
    #                     if morphedRange is not None:
    #                         pendingSeedRanges.append(morphedRange)
    #                 break

    #         if matched == False:
    #             pendingSeedRanges.append(seedRange)

    #     seedRanges = pendingSeedRanges
    #     # it's doubling the ranges

    
    # #part 2 - works but is very slow

    # if fileName == 'day5/day5_0.txt':
    #     assert mapSeedReverse(46, parsedMaps) == 82
    #     assert mapSeedReverse(82, parsedMaps) == 79
    #     assert mapSeedReverse(43, parsedMaps) == 14
    #     assert mapSeedReverse(86, parsedMaps) == 55
    #     assert mapSeedReverse(35, parsedMaps) == 13

    # # find the lowest by going backward - very slow
    # # lowestLocation = None
    # # location = 0
    # # while lowestLocation == None:
    # #     checkSeed = mapSeedReverse(location, parsedMaps)
    # #     if isValidSeed(checkSeed, seeds):
    # #         lowestLocation = location
    # #     else:
    # #         location += 1
    # # print(f'Part 2 lowest location going backward: {lowestLocation}')
        
    # # next idea - map and morph the seed ranges themselves
    
    # print(f'Part 2 lowest location : {lowestLocation}')

if __name__ == '__main__':
    main()
    
