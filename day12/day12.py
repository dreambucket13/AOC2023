# https://adventofcode.com/2023/day/12

class UnknownSection:
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
                self.unknownSections.append(UnknownSection(start, length))

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
        
def inSameSection(index1, index2, unknownSections) -> bool:

    #TODO - arbitrary length of indexes to check
    index1Section = None
    index2Section = None

    for sectionNum, unknownSection in enumerate(unknownSections):
        if index1 >= unknownSection.start and index1 <=unknownSection.end:
            index1Section = sectionNum
        if index2 >= unknownSection.start and index2 <=unknownSection.end:
            index2Section = sectionNum

    return index1Section == index2Section

def spaceAhead(springRecord, sectionToCheck ):

    # spaceahead is simply the length of the questioning section minus the length of the section.
    #assumes only one section is present in the questionable one.

    return springRecord.unknownSections[sectionToCheck] - springRecord.confirmedDamaged[sectionToCheck]

def combinationsInSameSection(damagedSectionsToCheck: list, springRecord: SpringRecord) ->int:

    # assume the list of sections are already in the same unknown area.

    #also assume current combination is already a valid one.
    combinations = 1 
    locations = [x for x in springRecord.damagedSectionLocations]
    lengths = [x for x in springRecord.confirmedDamaged]

    conditionRecord = springRecord.conditionRecord

    # start at last section
    # move until I hit an end stop
    # when you do, move prior section up 1 and reset current section to valid spot
    # if a section cannot move, set current to prior
    # if you run out of sections, you're done

    foundAllCombinations = False
    currentSectionId = damagedSectionsToCheck[-1]
    priorSectionId = currentSectionId - 1

    while foundAllCombinations == False:

        currentSectionLimit = locations[currentSectionId] + lengths[currentSectionId]
        priorSectionLimit = locations[priorSectionId] + lengths[priorSectionId]

        # print(f'curr: {locations[currentSectionId]}, prior: {locations[priorSectionId]}')

        # currently only works if last section will hit a wall, i.e. only 2 sections.
        if currentSectionLimit < len(conditionRecord):
            locations[currentSectionId] += 1
            combinations += 1
        else:
            # hit end stop
            if priorSectionLimit < locations[currentSectionId] - 1:
                locations[priorSectionId] += 1
                locations[currentSectionId] = priorSectionLimit + 2
                combinations += 1
            elif priorSectionId == damagedSectionsToCheck[0]:
                foundAllCombinations = True
            else:
                currentSectionId = priorSectionId
                priorSectionId = currentSectionId - 1
        
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
    
    validCombinations = combinationsInSameSection([1,2], springRecords[5])

    print(f'total combinations: {validCombinations}')

if __name__ == '__main__':
    part1('day12\day12_0.txt')
