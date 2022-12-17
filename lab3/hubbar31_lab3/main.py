# James Hubbard
# Lab 3
# ECE 40862

import esp32
import machine
import neopixel
import network
import ntptime

def do_connect(ssid, key=None): #directly from MicroPython docs
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
        print("Connected to", ssid)
        print('IP Address:', wlan.ifconfig()[0])

def modify_datetime(dt_tup, field, offset):
    dt = list(dt_tup)
    if (field == "hours"):
        dt[4] = dt[4] + offset
        if dt[4] < 0: # hours underflow
            dt[4] = dt[4] + 24
            dt[3] = dt[3] - 1
            dt[2] = dt[2] - 1
        if dt[3] < 0: # weekday underflow
            dt[3] = dt[3] + 7
        if dt[2] < 0: # day underflow
            pass # way too much effort to import a table of month lengths
    else:
        print("not implemented")

    return tuple(dt)

def touchTimerCallback(t):
    global np
    global TOUCH_THRESH
    global tp
    rd = tp.read()
    if rd < TOUCH_THRESH:
        np[0] = (0, 255, 0)
    else:
        np[0] = (0, 0, 0)
    np.write()

def displayDateTimeCallback(t):
    global rtc
    date = rtc.datetime()
    print("Date: %02d/%02d/%02s" % (date[0], date[1], date[2]))
    print("Time: %02d:%02d:%02d HRS" % (date[4], date[5], date[6]))

def sleepTimerCallback(t):
    global io13
    print("I am going to sleep for 1 minute.")
    io13.value(0)
    machine.deepsleep(6000)

# GLOBALS
io13 = machine.Pin(13, machine.Pin.OUT)
io33 = machine.Pin(33)
np_power = machine.Pin(2, machine.Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(0), 1)
rtc = machine.RTC()
timPrint = machine.Timer(1)
timSleep = machine.Timer(2)
timTouch = machine.Timer(3)
TOUCH_THRESH = 300;
tp = machine.TouchPad(machine.Pin(14))


def main():
    global io13
    global io33
    global np
    global np_power
    global rtc
    global timPrint
    global timSleep
    global timTouch
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        if machine.wake_reason() == machine.PIN_WAKE:
            print("Wake up due to EXT0 wakeup.")
        else:
            print("Wake up due to Timer wakeup.")
    # red LED on whenever awake
    io13.value(1)
    # Connect to wifi and report to the terminal
    do_connect("BV9500", "37744734231d")
    # Get the current time using NTP, set the RTC
    ntptime.host = "pool.ntp.org"
    try: 
        ntptime.settime()
    except:
        pass
    rtc.datetime(modify_datetime(rtc.datetime(), "hours", -4)) # "manually" set the timezone
    # Display date and time every 15 seconds
    timPrint.init(period=15000, callback=displayDateTimeCallback)
    # Check touch pin every 50 ms 
    np_power.value(1)
    timTouch.init(period=50, callback=touchTimerCallback)
    # 1 mintue deep sleep every 30 seconds, report to terminal
    timSleep.init(period=30000, callback=sleepTimerCallback)
    # Timer wakeup, external button (EXT0) wakeup
    esp32.wake_on_ext0(io33, esp32.WAKEUP_ANY_HIGH)
    pass

if __name__ == "__main__":
    main()
