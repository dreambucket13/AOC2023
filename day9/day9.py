# https://adventofcode.com/2023/day/9

def main():

    with open('day9/day9_1.txt') as input:
        inputLines = input.readlines()

    histories = []

    for line in inputLines:
        histories.append(list(map(int, line.split(' '))))
    
    totalExtrapolatedForward = 0

    for history in histories:
        totalExtrapolatedForward += extrapolateForward(history)

    print(totalExtrapolatedForward)

def extrapolateForward(history):

    deltaLines = []
    allZero = False
    currentLine = history
    deltaLines.append(history)

    while allZero == False:

        allZero = True
        deltas = []

        for index, value in enumerate(currentLine):
            if index == 0:
                continue
            delta = value - currentLine[index - 1]
            deltas.append(delta)

            if delta != 0:
                allZero = False
        
        deltaLines.append(deltas)

        currentLine = deltaLines[len(deltaLines) - 1]

    extrapolated = 0

    for line in reversed(deltaLines):
        extrapolated += line[-1]

    return extrapolated
    
if __name__ == '__main__':
    main()