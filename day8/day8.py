# https://adventofcode.com/2023/day/8


def main():

    with open('day8/day8_2.txt') as input:
        inputLines = input.readlines()
        
    turns = inputLines[0][:-1]

    nodes = {}
    
    for line in inputLines[2:]:
        lineData = line.split(" = ")
        nodeName = lineData[0]

        rightAndLeft = lineData[1].split(', ')
        left = rightAndLeft[0][1:]
        right = rightAndLeft[1][:-2]

        nodes[nodeName] = (left, right)


    ZZZfound = False
    currentNode = 'AAA'
    steps = 0

    while ZZZfound == False:

        for turn in turns:
            if turn == 'L':
                currentNode = nodes[currentNode][0]
            else:
                currentNode = nodes[currentNode][1]

            steps += 1

            if currentNode == 'ZZZ':
                ZZZfound = True
                break

    print(f'Steps: {steps}')
    
if __name__ == '__main__':
    main()