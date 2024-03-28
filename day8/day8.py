# https://adventofcode.com/2023/day/8

def main():

    with open('day8/day8_3.txt') as input:
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

    #part 2

    ZZZfound = False
    steps = 0

    while ZZZfound == False:

        for turn in turns:
            ZZZfound = True
            activeNodesTemp = []
            if turn == 'L':
                for node in part2ActiveNodes:
                    activeNodesTemp.append(nodes[node][0])
                    if node.endswith('Z') == False:
                        ZZZfound = False
            else:
                for node in part2ActiveNodes:
                    activeNodesTemp.append(nodes[node][1])
                    if node.endswith('Z') == False:
                        ZZZfound = False

            if ZZZfound == True:
                break

            steps += 1
            part2ActiveNodes = activeNodesTemp
            print(f'{part2ActiveNodes}')
            
    print(f'Part 2 steps: {steps}')
    
if __name__ == '__main__':
    main()