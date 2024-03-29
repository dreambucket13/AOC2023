# https://adventofcode.com/2023/day/8

import math

def main():

    with open('day8/day8_2.txt') as input:
        inputLines = input.readlines()
        
    turns = inputLines[0][:-1]

    nodes = {}
    part2ActiveNodes = []
    
    for line in inputLines[2:]:
        lineData = line.split(" = ")
        nodeName = lineData[0]

        if nodeName.endswith('A'):
            part2ActiveNodes.append(nodeName)

        rightAndLeft = lineData[1].split(', ')
        left = rightAndLeft[0][1:]
        right = rightAndLeft[1].replace(')', '').strip()

        nodes[nodeName] = (left, right)

    #part 2

    steps = 1
    periods = [0] * len(part2ActiveNodes) #steps to get to a Z
    #everything repeats....calculate the 'period' of each starting node then calculate when they align?

    for index, node in enumerate(part2ActiveNodes):
        ZZZfound = False
        currentNode = node
        while ZZZfound == False:

            for turn in turns:
                if turn == 'L':
                    currentNode = nodes[currentNode][0]
                else:
                    currentNode = nodes[currentNode][1]

                periods[index] += 1

                if currentNode.endswith('Z'):
                    ZZZfound = True
                    break

    print(f'periods: {periods}')

    steps = math.lcm(*periods)
        
    print(f'Part 2 steps: {steps}')

    #part 1
    # ZZZfound = False
    # currentNode = 'AAA'
    # steps = 0

    # while ZZZfound == False:

    #     for turn in turns:
    #         if turn == 'L':
    #             currentNode = nodes[currentNode][0]
    #         else:
    #             currentNode = nodes[currentNode][1]

    #         steps += 1

    #         if currentNode == 'ZZZ':
    #             ZZZfound = True
    #             break

    # print(f'Steps: {steps}')
    
if __name__ == '__main__':
    main()