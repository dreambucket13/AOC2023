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
            mapRange = mapIntegers[2]
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

    #part 2

    # uh...I can go backwards maybe.  instead of mapping seed to location, map location to seed.
    # starting from 0, the first location that maps to a seed should be the lowest. 

    #yep....got seed 82 from location going backward!

    if fileName == 'day5/day5_0.txt':
        assert mapSeedReverse(46, parsedMaps) == 82
        assert mapSeedReverse(82, parsedMaps) == 79
        assert mapSeedReverse(43, parsedMaps) == 14
        assert mapSeedReverse(86, parsedMaps) == 55
        assert mapSeedReverse(35, parsedMaps) == 13



    # location = 0

    # # write out the valid seed locations
    # while location <= 100:
    #     checkSeed = mapSeedReverse(location, parsedMaps)
    #     if isValidSeed(checkSeed, seeds):
    #         print(f'VALID seed at final location {location}')
    #     else:
    #         print(f'Invalid seed at final location {location}')

    mapSeedVerbose(82, parsedMaps)

    # map the seed to final locations
    lowestLocation = None
    for (seedNum, seed) in enumerate(seeds):
        if seedNum % 2 == 0:
            seedStart = seeds[seedNum]
            seedRange = seeds[seedNum+1]
            for x in range(seedStart, seedStart + seedRange):
                finalLocation = mapSeed(x, parsedMaps)
                if lowestLocation == None or finalLocation < lowestLocation:
                    lowestLocation = finalLocation
                # print(f'Seed {x}, final location {finalLocation}')
        else:
            continue
    print(f'Part 2 lowest location going forward: {lowestLocation}')

    # find the lowest by going backward
    lowestLocation = None
    location = 0
    while lowestLocation == None:
        checkSeed = mapSeedReverse(location, parsedMaps)
        if isValidSeed(checkSeed, seeds):
            lowestLocation = location
        else:
            location += 1

    print(f'Part 2 lowest location going backward: {lowestLocation}')

if __name__ == '__main__':
    main()
    
    # locationHighGuess = 0
    # locationLowGuess = 0
    # location = 1

    # #still too slow...try to get a basic high guess by doubling the location every iteration.

    # while locationHighGuess == 0 :

    #     backtrackedSeedNumber = mapSeedReverse(location, parsedMaps)

    #     if isValidSeed(backtrackedSeedNumber, seeds):
    #         locationHighGuess = location
    #         break
    #     else:
    #         locationLowGuess = location
    #         location *= 2

    # else:
    #     print('Did not find valid seed?')


    # assert isValidSeed(mapSeedReverse(locationLowGuess, parsedMaps), seeds) == False
    # assert isValidSeed(mapSeedReverse(locationHighGuess, parsedMaps), seeds) == True

    # #ok...I have a low and high guess.  binary search?
    
    # while locationLowGuess < locationHighGuess:
    #     print(f'low guess: {locationLowGuess}, high guess: {locationHighGuess}')
    #     location = (locationHighGuess + locationLowGuess) // 2

    #     backtrackedSeedNumber = mapSeedReverse(location, parsedMaps)

    #     if isValidSeed(backtrackedSeedNumber, seeds) == False:
    #         locationLowGuess = location
    #     else:
    #         locationHighGuess = location

    #     if locationHighGuess - locationLowGuess == 1:
    #         print(f'low guess {locationLowGuess} is {isValidSeed(mapSeedReverse(locationLowGuess, parsedMaps), seeds)}')
    #         print(f'high guess {locationHighGuess} is {isValidSeed(mapSeedReverse(locationHighGuess, parsedMaps), seeds)}')   
    #         lowestLocation = locationHighGuess         
    #         break
