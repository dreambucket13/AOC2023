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
        #print(f'seed: {seed}, map: {currentMap}, location: {location}')
        
    return location

def main():
    input = open('day5/day5_1.txt', 'r')
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

    # map the seeds
    lowestLocation = None
    for seed in seeds:

        location = mapSeed(seed, parsedMaps)

        if lowestLocation == None or location < lowestLocation:
            lowestLocation = location

    print(f'Lowest location: {lowestLocation}')

if __name__ == '__main__':
    main()
    

