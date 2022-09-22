#!/usr/bin/env python3

import datetime
import time

def main():
    name = input("What is your name? ")
    age = int(input("How old are you? "))
    date = datetime.date.today()
    year = date.year
    year = year + (100 - age)
    print(name, "will be 100 years old in the year", year, sep=" ")

if __name__ == '__main__':
    main()
