# https://adventofcode.com/2023/day/7

FIVE_OF_A_KIND = 70000000000
FOUR_OF_A_KIND = 60000000000
FULL_HOUSE = 50000000000
THREE_OF_A_KIND = 40000000000
TWO_PAIR = 30000000000
ONE_PAIR = 20000000000
HIGH_CARD = 10000000000

class Hand:
    handString: str
    primaryRank: int
    cardCounts: list
    fiveOfAKindCard = None
    fourOfAKindCard = None
    threeOfAKindCard = None
    twoOfAKindCards = []
    singleCards = []
    numJokers = 0
    maxMatches = 0

    def __init__(self, handStr):
        self.handString = handStr
        self.primaryRank = 0
        self.cardCounts = [0] * 15
        self.fiveOfAKindCard = None
        self.fourOfAKindCard = None
        self.threeOfAKindCard = None
        self.twoOfAKindCards = []
        self.singleCards = []
        self.numJokers = 0
        self.maxMatches = 0



        secondaryRankPower = 8
        for card in handStr:
            match card:
                case 'J': #J now Joker
                    self.cardCounts[1] += 1
                    self.primaryRank += 1 * pow(10,secondaryRankPower)
                case '2'  : 
                    self.cardCounts[2] += 1
                    self.primaryRank += 2 * pow(10,secondaryRankPower)
                case '3'  : 
                    self.cardCounts[3] += 1
                    self.primaryRank += 3 * pow(10,secondaryRankPower)
                case '4'  : 
                    self.cardCounts[4] += 1 
                    self.primaryRank += 4 * pow(10,secondaryRankPower)  
                case '5'  : 
                    self.cardCounts[5] += 1    
                    self.primaryRank += 5 * pow(10,secondaryRankPower)        
                case '6'  : 
                    self.cardCounts[6] += 1
                    self.primaryRank += 6 * pow(10,secondaryRankPower)  
                case '7'  : 
                    self.cardCounts[7] += 1
                    self.primaryRank += 7 * pow(10,secondaryRankPower)  
                case '8'  : 
                    self.cardCounts[8] += 1
                    self.primaryRank += 8 * pow(10,secondaryRankPower)  
                case '9'  : 
                    self.cardCounts[9] += 1
                    self.primaryRank += 9 * pow(10,secondaryRankPower)  
                case 'T' :    
                    self.cardCounts[10] += 1
                    self.primaryRank += 10 * pow(10,secondaryRankPower)                           
                case 'Q'  : 
                    self.cardCounts[11] += 1
                    self.primaryRank += 11 * pow(10,secondaryRankPower)                 
                case 'K'  : 
                    self.cardCounts[12] += 1
                    self.primaryRank += 12 * pow(10,secondaryRankPower)                  
                case 'A'  : 
                    self.cardCounts[13] += 1
                    self.primaryRank += 13 * pow(10,secondaryRankPower)   
                case _  : 
                    pass
            secondaryRankPower -= 2

        for card, count in enumerate(self.cardCounts):
            if count == 1:
                self.singleCards.append(card)
            if count == 2:
                self.twoOfAKindCards.append(card)
            if count == 3:
                self.threeOfAKindCard = card
            if count == 4:
                self.fourOfAKindCard = card
            if count == 5:
                self.fiveOfAKindCard = card  
        
        self.numJokers = self.cardCounts[1]
        self.maxMatches = max(self.cardCounts[2:])

        def assignPrimaryRank(self):
            if self.fiveOfAKindCard is not None or (self.numJokers + self.maxMatches == 5):
                self.primaryRank += FIVE_OF_A_KIND
                return

            if self.fourOfAKindCard is not None or (self.numJokers + self.maxMatches == 4):
                self.primaryRank += FOUR_OF_A_KIND
                return
            
            if  ((self.threeOfAKindCard is not None) and (len(self.twoOfAKindCards) == 1) or (len(self.twoOfAKindCards) == 2 and self.numJokers == 1) ):
                self.primaryRank += FULL_HOUSE
                return      

            if self.threeOfAKindCard is not None or (self.numJokers + self.maxMatches == 3):
                self.primaryRank += THREE_OF_A_KIND
                return      
            
            if len(self.twoOfAKindCards) == 2: #adding jokers to a 2 pair makes a full house or 4 of a kind
                self.primaryRank += TWO_PAIR
                return  
            
            if len(self.twoOfAKindCards) == 1 or self.numJokers == 1:
                self.primaryRank += ONE_PAIR
                return  
            
            self.primaryRank += HIGH_CARD
            return   
           
        assignPrimaryRank(self)
               
def parseInput(fileName):

    with open(fileName) as input:
        inputLines = input.readlines()
    
    gameData = []

    for line in inputLines:
        gameAndBid = line.split(' ')
        hand = Hand(gameAndBid[0])
        bid = int(gameAndBid[1])
        gameData.append( (hand,bid) )

    return gameData

def main():
    gameData = parseInput('day7/day7_1.txt')

    gameData.sort(key=lambda game: game[0].primaryRank)

    winnings = 0

    for (index, game) in enumerate(gameData):
        if game[0].numJokers > 0:
            print(f'hand: {game[0].handString}, rank: {game[0].primaryRank}, jokers: {game[0].numJokers}, matches: {game[0].maxMatches} ')
        winnings += (index + 1) * game[1]

    print(f'total winnings: {winnings}')
        

    pass
    
if __name__ == '__main__':
    main()