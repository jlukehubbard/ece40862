# James Hubbard
# Lab 3
# ECE 40862

import esp32
import machine
import neopixel
import network
import ntptime
import socket

def do_connect(ssid, key=None): #directly from MicroPython docs
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
        print("Connected to", ssid)
        print('IP Address:', wlan.ifconfig()[0])

def dataTimerCallback(t):
    global s
    do_connect("MrWiskers", "7lkr1192Rush")
    data = (esp32.raw_temperature(), esp32.hall_sensor())
    print(data)
    print(s.send(b'GET https://api.thingspeak.com/update?api_key=EVQDT0X5CVJN0MHX&field1='+repr(data[0])+'&field2='+repr(data[1])+'\r\n\r\n'))

# GLOBALS
timData = machine.Timer(1)
s = socket.socket()

def main():
    global timData
    # Connect to wifi and report to the terminal
    do_connect("MrWiskers", "7lkr1192Rush")
    addr = socket.getaddrinfo('api.thingspeak.com', 80)[0][-1]
    s.connect(addr)
    dataTimerCallback(timData)
    timData.init(period=30000, callback=dataTimerCallback)


if __name__ == "__main__":
    main()
