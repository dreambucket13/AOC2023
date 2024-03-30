# https://adventofcode.com/2023/day/9

def main():

    with open('day9/day9_0.txt') as input:
        inputLines = input.readlines()

    histories = []

    for line in inputLines:
        histories.append(list(map(int, line.split(' '))))
    
    pass

            
if __name__ == '__main__':
    main()