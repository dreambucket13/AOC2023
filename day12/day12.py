# https://adventofcode.com/2023/day/12

class SpringRecord:
    def __init__(self, conditionRecord, confirmedDamaged):
        self.conditionRecord = conditionRecord
        self.confirmedDamaged = confirmedDamaged

def analyzeRecord(springRecord: SpringRecord) -> int:
    combinations = 0

    unknownGroups = []

    confirmedGroups = []

    #first, determine which groups are confirmed?

    for spring in springRecord.conditionRecord:
        pass

    return combinations


def part1(file):

    with open(file) as input:
        inputLines = input.readlines()

    springRecords = []

    for line in inputLines:
        data = line.split(' ')

        confirmedDamaged = []

        for char in data[1]:
            if char.isnumeric():
                confirmedDamaged.append(int(char))

        springRecords.append(SpringRecord(data[0], confirmedDamaged))

    validCombinations = 0

    for springRecord in springRecords:
        validCombinations += analyzeRecord(springRecord)

    

if __name__ == '__main__':
    part1('day12\day12_0.txt')
