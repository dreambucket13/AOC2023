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
        self.unknownSections = []

        for index, char in enumerate(conditionRecord):
            if char == '?' and inSection == False:
                inSection = True
                start = index
            elif (char != '?' or index == len(conditionRecord)-1) and inSection == True:
                inSection = False
                length = index - start
                self.unknownSections.append(QuestionableSection(start, length))

        # find the 1st possible location for each section
        confirmedDamagedSectionNum = 0
        self.damagedSectionLocations = [0] * len(self.confirmedDamaged)
        index = 0

        initializedAllSections = False

        while initializedAllSections == False:

            confirmedDamagedSectionLength  = self.confirmedDamaged[confirmedDamagedSectionNum]
            doIFits = ifIFitsISits(conditionRecord, index, confirmedDamagedSectionLength)

            if doIFits == False:
                index += 1
            else:
                self.damagedSectionLocations[confirmedDamagedSectionNum] = index
                index += confirmedDamagedSectionLength + 1 #damaged sections can't be next to one another

                if confirmedDamagedSectionNum == len(self.confirmedDamaged) - 1:
                    initializedAllSections = True
                else:
                    confirmedDamagedSectionNum += 1

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

def newString(conditionRecord, index, confirmedDamagedSectionLength):
    return conditionRecord[:index] + ''.join(map(str, ([('@') for char in range(0,confirmedDamagedSectionLength)]))) + (conditionRecord[index + confirmedDamagedSectionLength:])
        

def analyzeRecord(springRecord: SpringRecord) -> int:

    conditionRecord = springRecord.conditionRecord

    damagedSectionLocations = springRecord.damagedSectionLocations
    confirmedDamagedSectionNum = len(damagedSectionLocations) - 1

    combinations = {}
    foundAllCombinations = False

    while foundAllCombinations == False:

        index = damagedSectionLocations[confirmedDamagedSectionNum]
        confirmedDamagedSectionLength  = springRecord.confirmedDamaged[confirmedDamagedSectionNum]

        doIFits = ifIFitsISits(conditionRecord, index, confirmedDamagedSectionLength)
        iCanMove = sectionCanMove(confirmedDamagedSectionNum, springRecord.confirmedDamaged, damagedSectionLocations, conditionRecord )
        
        if doIFits == True and tuple(damagedSectionLocations) not in combinations:
            combinations[tuple(damagedSectionLocations)] = True

        if iCanMove == True:
            doIFitsAgain = ifIFitsISits(conditionRecord, index + 1, confirmedDamagedSectionLength)
            if doIFitsAgain == True:
                index += 1
                damagedSectionLocations[confirmedDamagedSectionNum] = index
            else:
                if confirmedDamagedSectionNum == 0:
                    foundAllCombinations = True
                else:
                    confirmedDamagedSectionNum -= 1
                    index = damagedSectionLocations[confirmedDamagedSectionNum]
        else: 
            if confirmedDamagedSectionNum == 0:
                foundAllCombinations = True
            else:
                confirmedDamagedSectionNum -= 1
                index = damagedSectionLocations[confirmedDamagedSectionNum]

    return len(combinations)

def inSameSection(index1, index2, unknownSections):

    index1Section = None
    index2Section = None

    for sectionNum, unknownSection in enumerate(unknownSections):
        if index1 >= unknownSection.start and index1 <=unknownSection.end:
            index1Section = sectionNum
        if index2 >= unknownSection.start and index2 <=unknownSection.end:
            index2Section = sectionNum

    return index1Section == index2Section

def spaceAhead(springRecord, damagedSectionLocations ):

    spaceAheadOfSections = []
    conditionRecord = springRecord.conditionRecord
    damagedSectionLengths = springRecord.confirmedDamaged
    unknownSections = springRecord.unknownSections

    # space ahead = total space - sum(space occupied by later sections if they are part of contiguous ?? section + 1)

    damagedSectionNum = len(damagedSectionLengths) - 1

    # assert inSameSection(5,8,unknownSections) == True
    # assert inSameSection(1,8,unknownSections) == False
    # assert inSameSection(1,5,unknownSections) == False

    pendingSpaceAhead = 0

    while damagedSectionNum >= 0:
    # sections that start with '#' are locked
        slot = conditionRecord[damagedSectionLocations[damagedSectionNum]]
        index = damagedSectionLocations[damagedSectionNum] + damagedSectionLengths[damagedSectionNum]

        if damagedSectionNum < len(damagedSectionLocations) - 1 and inSameSection(damagedSectionLocations[damagedSectionNum], damagedSectionLocations[damagedSectionNum + 1], unknownSections):
            subtractedSpace = damagedSectionLengths[damagedSectionNum + 1] + 1
        else:
            subtractedSpace = 0

        if slot == '#' or index > len(conditionRecord) - 1:
            spaceConsumed = True
            spaceAheadOfSections.append(pendingSpaceAhead - subtractedSpace)
            pendingSpaceAhead = 0
            damagedSectionNum -= 1
        else:

            spaceConsumed = False

            while spaceConsumed == False:
                
                if index < len(conditionRecord):
                    slot = conditionRecord[index]
                else:
                    spaceConsumed = True
                    spaceAheadOfSections.append(pendingSpaceAhead - subtractedSpace)
                    pendingSpaceAhead = 0
                    damagedSectionNum -= 1
                    break

                if slot == '?':
                    pendingSpaceAhead += 1
                    index += 1
                else:
                    spaceConsumed = True
                    spaceAheadOfSections.append(pendingSpaceAhead - subtractedSpace)
                    pendingSpaceAhead = 0
                    damagedSectionNum -= 1

    spaceAheadOfSections.reverse()

    return spaceAheadOfSections

def analyzeRecordMultiplicative(springRecord: SpringRecord) -> int:

    damagedSectionLocations = springRecord.damagedSectionLocations

    additionalCombos = spaceAhead(springRecord, damagedSectionLocations)

    combinations = 1
    for additionalCombo in additionalCombos:
        if additionalCombo > 0:
            combinations *= additionalCombo

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

    # assert ifIFitsISits('.??..??...?##.', 10, 3) == True
    # assert ifIFitsISits('.??..??...?##.', 10, 5) == False
    # assert ifIFitsISits('.??..??...?##.', 10, 4) == False
    # assert ifIFitsISits('.??..??...?##.', 1, 1) == True
    # assert ifIFitsISits('.??..??...?##.', 2, 1) == True
    # assert ifIFitsISits('.??..??...?##.', 0, 1) == False
    # assert ifIFitsISits('?###????????', 0, 3 ) == False
    # assert ifIFitsISits('?###????????', 0, 4 ) == True
    # assert ifIFitsISits('?#?#?#?#?#?#?#?', 0, 6) == True

    # assert sectionCanMove(2, (1,1,3) , (0,2,4) , '???.###') == False

    # # ????.#...#... 4,1,1
    # assert sectionCanMove(0, (4,1,1) , (0,5,9) , '????.#...#...') == False
    # assert sectionCanMove(1, (4,1,1) , (0,5,9) , '????.#...#...') == True
    # assert sectionCanMove(2, (4,1,1) , (0,5,9) , '????.#...#...') == True
    # # .??..??...?##. 1,1,3
    # assert sectionCanMove(1, (1,1,3), (1,5,10), '.??..??...?##.') == True

    # assert ifIFitsISits('.??..??...?##.',5,1) == True
    # assert ifIFitsISits('.??..??...?##.',6,1) == True
    # assert ifIFitsISits('.??..??...?##.',7,1) == False

    # SPAAAACE = spaceAhead(springRecords[5], (1,5,8))
    # print(SPAAAACE)

    # SPAAAACE = spaceAhead(springRecords[1], (1,5,10))
    # print(SPAAAACE)

    # validCombinations += analyzeRecord(springRecords[1])
    
    validCombinations += analyzeRecordMultiplicative(springRecords[0])

    for springRecord in springRecords:
        pass

    print(f'total combinations: {validCombinations}')

if __name__ == '__main__':
    part1('day12\day12_0.txt')
