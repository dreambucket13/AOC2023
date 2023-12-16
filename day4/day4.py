# https://adventofcode.com/2023/day/4

import re
import bisect

input = open('day4/day4_1.txt', 'r')
games = input.readlines()
spaceDelimeter = re.compile(r'\s+')
colonAndSpaceDelimeter = re.compile(r':\s+')
totalPoints = 0
gameNum = 0

for game in games:
    gameData = game.split(" | ")
    winningNumbers = gameData[1]
    winningNumbersList = spaceDelimeter.split(winningNumbers)

    # sometimes we get an extra space if the 1st or last number is a single digit
    if winningNumbersList[0] == '':
        winningNumbersList = winningNumbersList[1:]

    if winningNumbersList[-1] == '':
        winningNumbersList = winningNumbersList[:-1]

    winningNumbersList = list(map(int, winningNumbersList))
    winningNumbersList.sort()

    myNumbers = colonAndSpaceDelimeter.split(gameData[0])[1]
    myNumbersList = spaceDelimeter.split(myNumbers)
    myNumbersList = list(map(int, myNumbersList))

    matches = 0

    for number in myNumbersList:
        i = bisect.bisect_left(winningNumbersList, number)
        if i < len(winningNumbersList) and i >= 0 and winningNumbersList[i] == number:
            #print(f'Game {game} matched number {winningNumbersList[i]} at index {i}')
            matches += 1

    points = 0
    if matches > 0:
        points = 1 * pow(2, matches - 1)
        totalPoints += points

    print(f'Game {gameNum} matches {matches}, points: {points}')
    gameNum += 1

print(f'Total points: {totalPoints}')
