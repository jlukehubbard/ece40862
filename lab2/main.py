# Lab2 hubbar31

import machine

rtc = machine.RTC()
sw38 = machine.Pin(38, machine.Pin.IN) # button
a2 = machine.Pin(34) # adc in pin
io12 = machine.Pin(12) # pwm out pin
adc = machine.ADC(a2, atten=machine.ADC.ATTN_11DB)
pwm = machine.PWM(io12)
timPrint = machine.Timer(1)
timADC = machine.Timer(2)
mode = -1
reading = 0
frequency = 10
duty = 32768
wait = 0

def getTimeFromUser():
    year = int(input("Year? "))
    month = int(input("Month? "))
    day = int(input("Day? "))
    weekday = int(input("Weekday? "))
    hours = int(input("Hours? "))
    minutes = int(input("Minutes? "))
    seconds = int(input("Seconds? "))
    subseconds = int(input("Microseconds? "))
    return (year, month, day, weekday, hours, minutes, seconds, subseconds)

def getTimeHardcoded():
    year = 2022
    month = 10
    day = 4
    weekday = 1
    hours = 20
    minutes = 20
    seconds = 0
    subseconds = 12345
    return (year, month, day, weekday, hours, minutes, seconds, subseconds)

def displayDateTimeCallback(t):
    date = rtc.datetime()
    print("%02d-%02d-%02s" % (date[0], date[1], date[2]), end=" ")
    print("%02d:%02d:%02d" % (date[4], date[5], date[6]))

def ADCCallback(t):
    global mode
    global pwm
    global adc
    global wait

    wait = 0 # reset the wait time for the button debouncing, easier than using a second timer and the period of this timer is reasonable for debouncing

    reading = adc.read_u16()
    if (mode == 0): # change freq
        pwm.freq((reading >> 10) + 1)
    elif (mode == 1): # change duty cycle
        pwm.duty_u16(reading)
    else: # do nothing (only happens at the beginning)
        pass

def switchCallback(p):
    global mode
    global wait
    if (wait == 0):
        wait = 1
        mode += 1
        mode %= 2


def main():
    global rtc
    global sw38
    global a2
    global io12
    global adc
    global pwm
    global timPrint
    global timADC
    global reading
    global frequency
    global duty

    # rtc.datetime(getTimeFromUser())
    rtc.datetime(getTimeHardcoded())

    #set default PWM params
    pwm.freq(frequency)
    pwm.duty_u16(duty)

    # Setup timer interrupt for displaying date and time every 30 seconds 
    timPrint.init(period=30000, callback=displayDateTimeCallback)

    # Setup 100ms timer interrupt to read potentiometer values on ADC1
    timADC.init(period=100, callback=ADCCallback)

    # Detect switch presses with another interrupt
    sw38.irq(handler=switchCallback, trigger=machine.Pin.IRQ_FALLING)
 

if __name__ == "__main__":
    main()
