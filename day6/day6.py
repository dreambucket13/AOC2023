# https://adventofcode.com/2023/day/6

import re
from dataclasses import dataclass
import math

@dataclass
class RaceData:
    time: int
    distanceRecord: int

    def CalculateDistance(self, buttonTime: int):
        velocity = buttonTime
        raceTime = self.time - buttonTime
        distanceTravelled = velocity * raceTime

        return distanceTravelled
    



def parseInput(fileName):

    with open(fileName) as input:
        inputLines = input.readlines()

    times = []
    distances = []

    for line in inputLines:
        if line.startswith('Time'):
            times = list(map(int,re.findall(r'\d+',line)))
        elif line.startswith('Distance'):
            distances = list(map(int,re.findall(r'\d+',line)))

    raceData = []

    for (time, distance) in zip(times, distances):
        raceData.append(RaceData(time,distance))

    return raceData

def main():
    raceData = parseInput('day6/day6_1.txt')
    
    totalWaysToBeatRecord = []
    beatRecord = 0

    for race in raceData:
        for buttonData in range(0,race.time + 1):
            if race.CalculateDistance(buttonData) > race.distanceRecord:
                beatRecord += 1
        totalWaysToBeatRecord.append(beatRecord)
        beatRecord = 0

    finalNumber = totalWaysToBeatRecord[0]

    for item in totalWaysToBeatRecord[1:]:
        finalNumber = finalNumber * item

    print(finalNumber)

    #part2
    # Time:        45     98     83     73
    # Distance:   295   1734   1278   1210

    raceData = RaceData(45988373, 295173412781210)

    #distance travelled = buttonTime * (total time - buttonTime)
    #                   = buttonTime^2 - buttonTime*totaltime

    # y = distance travelled, z = record, x = buttonTime, a = total race time
    #  we want y - z to be positive.
    #                 y = ((x) * (a - x)) 
    #                 y - z = ((x) * (a - x)) - z
    #                 0 = -x^2 + ax - z
    #                 quadratic eq where a = -1, b = totalTime (aka a here), c = record (z)
    # calculate zero intercepts for this equation

    #     Time:        45     98     83     73
    # Distance:   295   1734   1278   1210

    a = -1
    # b = 71530
    # c = -940200
    b = 45988373
    c = -295173412781210
    x1 = (-1*b + math.sqrt(b*b - 4*a*c))/(2*a)
    x2 = (-1*b - math.sqrt(b*b - 4*a*c))/(2*a)

    x1 = math.ceil(x1)
    x2 = math.floor(x2)

    print(f'x1: {x1}, x2: {x2}, total num ways: {x2-x1+1}')
    
if __name__ == '__main__':
    main()