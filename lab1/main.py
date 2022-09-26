#!/bin/python3

import machine
import time

def toggle(p):
    p.value(not p.value())

def main():
    p = machine.Pin(13, machine.Pin.OUT)
    for i in range(5):
        toggle(p)
        time.sleep(0.25)
        toggle(p)
        time.sleep(0.25)



if __name__ == "__main__":
    main()
