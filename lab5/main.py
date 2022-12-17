# James Hubbard
# Lab 3
# ECE 40862

import esp32
import machine
import neopixel
import network
import ntptime
import socket
import time
import urequests

wifi_SSID = "MrWiskers"
wifi_PASS = "7lkr1192Rush"
test_URL = "http://wifitest.adafruit.com/testwifi/index.html"
armed = False

#Credits: Andrew Lynn (former ECE40862 student) and Vijay R.
class MPU:
# Static MPU memory addresses
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F
    TEMP = 0x41
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47
    
    def acceleration(self):
        self.i2c.start()
        acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        # Accelerometer by default is set to 2g sensitivity setting
        # 1g = 9.81 m/s^2 = 16384 according to mpu datasheet
        acc_x = self.__bytes_to_int(acc_x) / 16384 * 9.81
        acc_y = self.__bytes_to_int(acc_y) / 16384 * 9.81
        acc_z = self.__bytes_to_int(acc_z) / 16384 * 9.81

        return acc_x, acc_y, acc_z

    def temperature(self):
        self.i2c.start()
        temp = self.i2c.readfrom_mem(self.addr, self.TEMP, 2)
        self.i2c.stop()

        temp = self.__bytes_to_int(temp)
        return self.__celsius_to_fahrenheit(temp / 340 + 36.53)

    def gyro(self):
        return self.pitch, self.roll, self.yaw

    def __init_gyro(self):
        # MPU must be stationary
        gyro_offsets = self.__read_gyro()
        self.pitch_offset = gyro_offsets[1]
        self.roll_offset = gyro_offsets[0]
        self.yaw_offset = gyro_offsets[2]

    def __read_gyro(self):
        self.i2c.start()
        gyro_x = self.i2c.readfrom_mem(self.addr, MPU.GYRO_X, 2)
        gyro_y = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Y, 2)
        gyro_z = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Z, 2)
        self.i2c.stop()

        # Gyro by default is set to 250 deg/sec sensitivity
        # Gyro register values return angular velocity
        # We must first scale and integrate these angular velocities over time before updating current pitch/roll/yaw
        # This method will be called every 100ms...
        gyro_x = self.__bytes_to_int(gyro_x) / 131 * 0.1
        gyro_y = self.__bytes_to_int(gyro_y) / 131 * 0.1
        gyro_z = self.__bytes_to_int(gyro_z) / 131 * 0.1

        return gyro_x, gyro_y, gyro_z

    def __update_gyro(self, timer):
        gyro_val = self.__read_gyro()
        self.pitch += gyro_val[1] - self.pitch_offset
        self.roll += gyro_val[0] - self.roll_offset
        self.yaw += gyro_val[2] - self.yaw_offset

    @staticmethod
    def __celsius_to_fahrenheit(temp):
        return temp * 9 / 5 + 32

    @staticmethod
    def __bytes_to_int(data):
        # Int range of any register: [-32768, +32767]
        # Must determine signing of int
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

    def __init__(self, i2c):
        # Init MPU
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107,0]))
        self.i2c.stop()
        print('Initialized MPU6050.')

        # Gyro values will be updated every 100ms after creation of MPU object
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_offset = 0
        self.__init_gyro()
        gyro_timer = machine.Timer(3)
        gyro_timer.init(mode=machine.Timer.PERIODIC, callback=self.__update_gyro, period=100)

def do_connect(ssid, key=None): #directly from MicroPython docs
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
        print("Connected to", ssid)
        print('IP Address:', wlan.ifconfig()[0])
    gc.collect()

baseline = tuple()
def gyroTimerCallback(t):
    global armed
    global mpu
    global baseline
    if (armed):
        val = mpu.acceleration()
        flag = False
        if val[0] <= (baseline[0] - 2) or val[0] >= (baseline[0] + 2):
            flag = True
        if val[1] <= (baseline[1] - 2) or val[1] >= (baseline[1] + 2):
            flag = True
        if val[2] <= (baseline[2] - 2) or val[2] >= (baseline[2] + 2):
            flag = True
        if flag:
            makeMovedRequest()
            armed = False
    else:
        baseline = mpu.acceleration()
        

def dataTimerCallback(t):
    global armed
    global np
    global np_power
    global wifi_SSID
    global wifi_PASS
    np_power.value(1)
    do_connect(wifi_SSID, wifi_PASS)
    # Check ThingSpeak
    resp = dict(readActivated())
    if (resp['feeds'][-1]['field1'] == '1'):
        armed = True
        np[0] = (0, 127, 0)
    else:
        armed = False
        np[0] = (0, 0, 0)
    print("Armed:", armed)
    np.write()
    gc.collect()

def makeMovedRequest():
    global np
    path = 'http://maker.ifttt.com/trigger/moved/with/key/lZAD4_OOBswWJOc0lYCamTHKU3WPpAnPLxtXysZLCdW'
    urequests.get(path)
    np[0] = (127, 0, 0)
    np.write()
    gc.collect()

def readActivated():
    url = "https://api.thingspeak.com/channels/1982516/fields/1.json?api_key=2H8QL4XLSPBSUSDF&results=2"
    try:
        response = urequests.get(url)
    except Exception as e:
        print(e)
        print("in readActivated")
    ret = response.json()
    response.close()
    gc.collect()
    return ret

def wifiTest():
    response = urequests.get(test_URL)
    print(response.text)
    response.close()
    gc.collect()

def socketWifiTest():
    endl = ' \r\n\r\n'
    try:
        addr = socket.getaddrinfo(test_URL, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET ' + test_URL + endl, 'utf-8'))
        ret = s.recv(256)
        print(str(ret))
        s.close()
    except Exception as e:
        print(e)
        print("in socketWifiTest")
    gc.collect()

def initGyro():
    global mpu
    global i2c
    mpu = MPU(i2c)
    

# GLOBALS
timData = machine.Timer(1)
timGyro = machine.Timer(2)
np_power = machine.Pin(2, machine.Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(0), 1)
i2c = machine.SoftI2C(scl=machine.Pin(14), sda=machine.Pin(22))
mpu = None


def main():
    global armed
    global np_power
    global timData
    global timGyro
    global wifi_SSID
    global wifi_PASS
    global mpu
    gc.enable()
    # Connect to wifi and report to the terminal
    print(wifi_SSID, wifi_PASS)
    gc.collect()
    np_power.value(1)
    do_connect(wifi_SSID, wifi_PASS)
    time.sleep(1)
    try:
        wifiTest()
    except:
        socketWifiTest()

    initGyro()
    timGyro.init(period=500, callback=gyroTimerCallback)
    timData.init(period=10000, callback=dataTimerCallback)

if __name__ == "__main__":
    main()
