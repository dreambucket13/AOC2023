# https://adventofcode.com/2023/day/4

import re
import bisect

input = open('day4/day4_0.txt', 'r')
games = input.readlines()
spaceDelimeter = re.compile(r'\s+')

for game in games:
    gameData = game.split(" | ")
    winningNumbers = gameData[1]
    winningNumbersList = spaceDelimeter.split(winningNumbers[:-1])
    winningNumbersList = list(map(int, winningNumbersList))
    winningNumbersList.sort()

    myNumbers = gameData[0].split(": ")[1]
    myNumbersList = spaceDelimeter.split(myNumbers)
    # TODO handle 1st number having only 1 digit
    myNumbersList = list(map(int, myNumbersList))

    for number in myNumbersList:
        i = bisect.bisect_left(winningNumbersList, number)
        if i < len(winningNumbersList):
            #it's in the list
            pass

    pass
