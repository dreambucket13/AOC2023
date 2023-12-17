# https://adventofcode.com/2023/day/4

import re
import bisect

def getMatches(myNumbersList, winningNumbersList):
    matches = 0
    for number in myNumbersList:
        i = bisect.bisect_left(winningNumbersList, number)
        if i < len(winningNumbersList) and i >= 0 and winningNumbersList[i] == number:
            matches += 1
    return matches

input = open('day4/day4_1.txt', 'r')
games = input.readlines()
spaceDelimeter = re.compile(r'\s+')
colonAndSpaceDelimeter = re.compile(r':\s+')
totalPoints = 0
card = 1

parsedCards = []
matchCache = []

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

    matches = getMatches(myNumbersList, winningNumbersList)
    matchCache.append(matches)

    points = 0
    if matches > 0:
        points = 1 * pow(2, matches - 1)
        totalPoints += points

    #print(f'Card {card} matches {matches}, points: {points}')
    card += 1

    parsedCards.append((myNumbersList, winningNumbersList))

print(f'Total points: {totalPoints}')

totalCards = 0

# cache the number of matches a card has
for (index, card) in enumerate(parsedCards):
    cardsInHand = [index]
    nextHand = []
    totalCards += 1

    while len(cardsInHand) > 0:
        for cardNum in cardsInHand:
            numbers = parsedCards[cardNum][0]
            winningNumbers = parsedCards[cardNum][1]
            matches = matchCache[cardNum]
            for i in range(1, matches + 1):
                nextHand.append(cardNum + i)
                totalCards += 1
            # print(f'Initial Card: {index}. Processing card {cardNum}, Next: {nextHand}')
            
        cardsInHand = nextHand
        nextHand = []

print(f'Total cards: {totalCards}')


    
