import machine
import neopixel

def switchpress():
    sw38 = machine.Pin(38, machine.Pin.IN)
    np_power = machine.Pin(2, machine.Pin.OUT)
    np = neopixel.NeoPixel(machine.Pin(0), 1)

    np_power.value(1)
    i = 0
    while i < 5:
        while not sw38.value():
            pass
        np[0] = (0, 255, 0)
        np.write()
        while sw38.value():
            pass
        np[0] = (255, 0, 0)
        np.write()
        i += 1

    np_power.value(0)
    print("You have successfully implemented LAB!")

if __name__ == "__main__":
    switchpress()
