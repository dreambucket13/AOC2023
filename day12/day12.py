# https://adventofcode.com/2023/day/12

class QuestionableSection:
    def __init__ (self, start, length):
        self.start = start
        self.length = length
        self.end = start + length - 1

class SpringRecord:
    def __init__(self, conditionRecord, confirmedDamaged):
        self.conditionRecord = conditionRecord
        self.confirmedDamaged = confirmedDamaged

        inSection = False
        self.questionableSections = []

        for index, char in enumerate(conditionRecord):
            if char == '?' and inSection == False:
                inSection = True
                start = index
            elif (char != '?' or index == len(conditionRecord)-1) and inSection == True:
                inSection = False
                length = index - start
                self.questionableSections.append(QuestionableSection(start, length))

def isValidPlacement(conditionRecord, start, damagedSectionlength):


    foundSectionLength = 0
    index = start
    char = conditionRecord[index]

    if start + damagedSectionlength > len(conditionRecord):
        return False
    elif char not in ('?', '#'):
        return False
    elif damagedSectionlength < 1:
        return False


    sectionEnd = False

    while sectionEnd == False and index < len(conditionRecord):
        if char == '?':

            if foundSectionLength >= damagedSectionlength:
                sectionEnd = True
                break

            foundSectionLength += 1
            index += 1
        elif char == '#':
            foundSectionLength += 1
            index += 1 
        elif char == '.' or index + 1 >= len(conditionRecord):
            sectionEnd = True

        char = conditionRecord[index]

    return foundSectionLength == damagedSectionlength

           

def analyzeRecord(springRecord: SpringRecord) -> dict:
    combinations = 0

    conditionRecord = springRecord.conditionRecord
    confirmedDamagedSectionLength  = springRecord.confirmedDamaged[0]

    usedPositions = [[] for damagedSection in springRecord.confirmedDamaged]

    index = 0
    foundAllCombinations = False




    # while foundAllCombinations == False:
    #     pass




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

    assert isValidPlacement('.??..??...?##.', 10, 3) == True
    assert isValidPlacement('.??..??...?##.', 10, 5) == False
    assert isValidPlacement('.??..??...?##.', 10, 4) == False
    assert isValidPlacement('.??..??...?##.', 1, 1) == True
    assert isValidPlacement('.??..??...?##.', 2, 1) == True
    assert isValidPlacement('.??..??...?##.', 0, 1) == False
    assert isValidPlacement('?###????????', 0, 3 ) == False
    assert isValidPlacement('?###????????', 0, 4 ) == True

    for springRecord in springRecords:
        validCombinations += analyzeRecord(springRecord)

    

if __name__ == '__main__':
    part1('day12\day12_0.txt')
