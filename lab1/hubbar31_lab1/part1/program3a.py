#!/usr/bin/env python3

def main():
    num = int(input("How many Fibonacci numbers would you like to generate? "))
    print("The Fibonacci Sequence is: ", end="")
    i = 0
    fib = list()
    fib.append(1)
    fib.append(1)
    print("1, 1", end="")
    i += 2
    while (i < num):
        fib.append(fib[i - 1] + fib[i - 2])
        print(", ", fib[i], sep="", end="")
        i += 1
    print("", end="\n")



if __name__ == '__main__':
    main()
