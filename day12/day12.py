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

def ifIFitsISits(conditionRecord, start, damagedSectionlength):

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
        
        if index < len(conditionRecord):
            char = conditionRecord[index]

    return foundSectionLength == damagedSectionlength

def sectionCanMove(sectionNum, confirmedDamagedSections, damagedSectionLocations, conditionRecord):
    if sectionNum == len(confirmedDamagedSections) - 1:
        # last section, limit is the end of the record
        if damagedSectionLocations[sectionNum] + confirmedDamagedSections[sectionNum] < len(conditionRecord) - 1:
            return True
        else:
            return False
        
    else:
        # limit is the location of the section ahead
        if damagedSectionLocations[sectionNum] + confirmedDamagedSections[sectionNum] < damagedSectionLocations[sectionNum + 1] - 2:
            return True
        else:
            return False
        
def analyzeRecord(springRecord: SpringRecord) -> int:

    conditionRecord = springRecord.conditionRecord

    confirmedDamagedSectionNum = 0

    damagedSectionLocations = [0] * len(springRecord.confirmedDamaged)

    index = 0

    # find the 1st possible location for each section

    initializedAllSections = False

    while initializedAllSections == False:

        confirmedDamagedSectionLength  = springRecord.confirmedDamaged[confirmedDamagedSectionNum]
        doIFits = ifIFitsISits(conditionRecord, index, confirmedDamagedSectionLength)

        if doIFits == False:
            index += 1
        else:
            damagedSectionLocations[confirmedDamagedSectionNum] = index
            index += 2 #damaged sections can't be next to one another

            if confirmedDamagedSectionNum == len(springRecord.confirmedDamaged) - 1:
                initializedAllSections = True
            else:
                confirmedDamagedSectionNum += 1

    
    combinations = {}
    combinations[tuple(damagedSectionLocations)] = True
    foundAllCombinations = False

    while foundAllCombinations == False:

        index = damagedSectionLocations[confirmedDamagedSectionNum]
        confirmedDamagedSectionLength  = springRecord.confirmedDamaged[confirmedDamagedSectionNum]

        doIFits = ifIFitsISits(conditionRecord, index, confirmedDamagedSectionLength)
        iCanMove = sectionCanMove(confirmedDamagedSectionNum, springRecord.confirmedDamaged, damagedSectionLocations, conditionRecord )

        # yucky one liner...
        newString = conditionRecord[:index] + ''.join(map(str, ([('@') for char in range(0,confirmedDamagedSectionLength)]))) + (conditionRecord[index + confirmedDamagedSectionLength:])

        # sections that cannot move do not add to the number of combos
        if doIFits == True and (sectionHasMoved == True or iCanMove == True):
            combinations += 1

        if iCanMove == True:
            index += 1
            damagedSectionLocations[confirmedDamagedSectionNum] = index
            sectionHasMoved = True
        else: 
            if confirmedDamagedSectionNum == 0:
                foundAllCombinations = True
            else:
                confirmedDamagedSectionNum -= 1
                index = damagedSectionLocations[confirmedDamagedSectionNum]
                sectionHasMoved = False

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

    assert ifIFitsISits('.??..??...?##.', 10, 3) == True
    assert ifIFitsISits('.??..??...?##.', 10, 5) == False
    assert ifIFitsISits('.??..??...?##.', 10, 4) == False
    assert ifIFitsISits('.??..??...?##.', 1, 1) == True
    assert ifIFitsISits('.??..??...?##.', 2, 1) == True
    assert ifIFitsISits('.??..??...?##.', 0, 1) == False
    assert ifIFitsISits('?###????????', 0, 3 ) == False
    assert ifIFitsISits('?###????????', 0, 4 ) == True
    assert ifIFitsISits('?#?#?#?#?#?#?#?', 0, 6) == True

    assert sectionCanMove(2, (1,1,3) , (0,2,4) , '???.###') == False

    # ????.#...#... 4,1,1
    assert sectionCanMove(0, (4,1,1) , (0,5,9) , '????.#...#...') == False
    assert sectionCanMove(1, (4,1,1) , (0,5,9) , '????.#...#...') == True
    assert sectionCanMove(2, (4,1,1) , (0,5,9) , '????.#...#...') == True
    # .??..??...?##. 1,1,3
    assert sectionCanMove(1, (1,1,3), (1,5,10), '.??..??...?##.') == True

    assert ifIFitsISits('.??..??...?##.',5,1) == True
    assert ifIFitsISits('.??..??...?##.',6,1) == True
    assert ifIFitsISits('.??..??...?##.',7,1) == False


    # validCombinations += analyzeRecord(springRecords[1])

    for springRecord in springRecords:
        addedCombinations = analyzeRecord(springRecord)
        print(f'line combinations: {addedCombinations}')
        validCombinations += addedCombinations

    print(f'total combinations: {validCombinations}')

if __name__ == '__main__':
    part1('day12\day12_0.txt')
