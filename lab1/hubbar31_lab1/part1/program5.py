#!/usr/bin/env python3

MAGIC_LIST = [10, 20, 10, 40, 50, 60, 70]

class PairSum:
    def __init__(self, num_list):
        self.num_list = num_list

    def pairSum(self, target):
        tot = 0
        for i, item1 in enumerate(self.num_list):
            for j, item2 in enumerate(self.num_list):
                tot = item1 + item2
                if (tot == target):
                    return (i, j)
        return (-1, -1)
    
    def printList(self):
        print(self.num_list)

def main():
    ps = PairSum(MAGIC_LIST)
    ps.printList()
    i = j = 0
    num = int(input("What's your target number? "))
    (i, j) = ps.pairSum(num)
    print("index1=", i, ", ", "index2=", j, sep="")

if __name__ == '__main__':
    main()
