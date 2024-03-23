# https://adventofcode.com/2023/day/6

import re
from dataclasses import dataclass

@dataclass
class RaceData:
    time: int
    distanceRecord: int

    def CalculateDistance(self, buttonTime: int):
        velocity = buttonTime
        raceTime = self.time - buttonTime
        distanceTravelled = velocity * raceTime

        #distance travelled = buttonTime * (total time - buttonTime)
        #                   = buttonTime^2 - buttonTime*totaltime

        # y = distance travelled, z = record, x = buttonTime, a = total race time
        #                 y - z = x^2 - a*x 
        #                 y = x^2 - a*x + z
        # calculate zero intercepts for this equation

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
    
if __name__ == '__main__':
    main()