# James Hubbard
# Lab 3
# ECE 40862

import esp32
import machine
import neopixel
import network
import ntptime
import socket

wifi_SSID = "BV9500"
wifi_PASS = "test1234"

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
    global wifi_SSID, wifi_PASS
    do_connect(wifi_SSID, wifi_PASS)
    data = (esp32.raw_temperature(), esp32.hall_sensor())
    print(data)
    print(s.send(b'https://maker.ifttt.com/trigger/moved/with/key/lZAD4_OOBswWJOc0lYCamTHKU3WPpAnPLxtXysZLCdW'+'\r\n\r\n'))

# GLOBALS
timData = machine.Timer(1)
s = socket.socket()

def main():
    global timData
    # Connect to wifi and report to the terminal
    do_connect(wifi_SSID, wifi_PASS)
    addr = socket.getaddrinfo('api.thingspeak.com', 80)[0][-1]
    s.connect(addr)
    dataTimerCallback(timData)
    timData.init(period=30000, callback=dataTimerCallback)


if __name__ == "__main__":
    main()
