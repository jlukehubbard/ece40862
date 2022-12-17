import esp32
import machine
import neopixel
import network
import ntptime
import socket


# Global variables
temp = 0  # measure temperature sensor data
hall = 0  # measure hall sensor data
red_led_state = str() # string, check state of red led, ON or OFF
s = socket.socket()
io13 = machine.Pin(13, machine.Pin.OUT)


def do_connect(ssid, key=None): #directly from MicroPython docs
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
        print("Connected to", ssid)
        print('IP Address:', wlan.ifconfig()[0])

def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    global temp
    global hall
    global red_led_state

    temp, hall = esp32.raw_temperature(), esp32.hall_sensor()
    if (io13.value()):
        red_led_state = "ON"
    else:
        red_led_state = "OFF"
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage

def main():
    global timData
    global s
    # Connect to wifi and report to the terminal
    do_connect("MrWiskers", "7lkr1192Rush")
    s.bind(('', 80))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        led_on = request.find('/?red_led=on')
        led_off = request.find('/?red_led=off')
        if led_on == 6:
            io13.value(1)
        if led_off == 6:
            io13.value(0)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

if __name__ == "__main__":
    main()

