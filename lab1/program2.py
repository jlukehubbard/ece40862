#!/usr/bin/env python3

def main():
    a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    print("a = ", a)
    num = int(input("Enter number: "))
    newlist = [i for i in a if i < num]
    print("The new list is ", newlist)

if __name__ == '__main__':
    main()
