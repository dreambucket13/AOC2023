# https://adventofcode.com/2023/day/5

import re

def getMap(mapName: str, almanac: list, lineNum: int):

    if almanac[lineNum].startswith(mapName):

        mapLineNum = lineNum + 1
        mapLine = almanac[mapLineNum]

        conversionMap = []

        while not mapLine.startswith('\n'):

            if mapLine[-1] == '\n':
                mapLine = mapLine[:-1]

            mapIntegers = list(map(int, mapLine.split(" ")))
            conversionMap.append(mapIntegers)

            if mapLineNum + 1 < len(almanac):
                mapLineNum += 1
                mapLine = almanac[mapLineNum]
            else:
                break

        return conversionMap
    else:
        return None


def main():
    input = open('day5/day5_0.txt', 'r')
    almanac = input.readlines()

    maps = {}
    mapTypes = ('seed-to-soil map:',
                'soil-to-fertilizer map:',
                'fertilizer-to-water map:',
                'water-to-light map:',
                'light-to-temperature map:',
                'temperature-to-humidity map:',
                'humidity-to-location map:')

    # parse
    for (lineNum, line) in enumerate(almanac):

        if line.startswith('seeds:'):
            seedLine = line.split(": ")[1][:-1] #remove newline char
            seeds = list(map(int, seedLine.split(" ")))
            continue

        for mapType in mapTypes:
            parsedMap = getMap(mapType, almanac, lineNum)
            if parsedMap != None:
                maps[mapType] = parsedMap

    pass

if __name__ == '__main__':
    main()
    

