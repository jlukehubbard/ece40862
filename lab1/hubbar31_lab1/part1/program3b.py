#!/usr/bin/env python3

import time

def main():
    rand = time.time_ns() % 11
    print(rand)
    guess = -1
    i = 0
    while ((guess != rand) and (i < 3)):
        guess = int(input("Enter your guess:"))
        i += 1

    print("You win!") if (guess == rand) else print("You lose!")

if __name__ == '__main__':
    main()
