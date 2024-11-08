from microdot import Microdot
from microdot.websocket import with_websocket
from microdot.cors import CORS
from machine import Pin, PWM
import asyncio 
import network
import time
import json

d2 = Pin(2, Pin.OUT)
d1 = Pin(18, Pin.OUT)
servo1 = machine.PWM(machine.Pin(17))   # Servo
servo1.freq(50)

# Initialize PWM and direction pins
PWM1 = PWM(Pin(3, Pin.OUT), freq=1000)  # Motor1
PWM2 = PWM(Pin(11, Pin.OUT), freq=1000)  # Motor2
PWM3 = PWM(Pin(27, Pin.OUT), freq=1000) # Motor 3
PWM4 = PWM(Pin(19, Pin.OUT), freq=1000) # Motor 4

#if 1, goes forward, if 2, goes backward

#Motor 4
frontLeft1 = Pin(21, Pin.OUT) #forward
frontLeft2  = Pin(20, Pin.OUT) #backward

#Motor 1
frontRight1 = Pin(10, Pin.OUT)
frontRight2 = Pin(0, Pin.OUT)

#Motor 3
backLeft1 = Pin(26, Pin.OUT)
backLeft2 = Pin(22, Pin.OUT)

#Motor 2
backRight1 = Pin(9, Pin.OUT)
backRight2 = Pin(5, Pin.OUT)

def servo_90():
    servo1.duty_u16(int((1550 / 20000) * 65535))
    time.sleep(1)

def servo_180():
    servo1.duty_u16(int((2500 / 20000) * 65535))
    time.sleep(1)

def allOff():
    frontLeft1.low()
    frontLeft2.low()
    frontRight1.low()
    frontRight2.low()
    backLeft1.low()
    backLeft2.low()
    backRight1.low()
    backRight2.low()
    PWM1.duty_u16(0)
    PWM2.duty_u16(0)
    PWM3.duty_u16(0)
    PWM4.duty_u16(0)

def pwmOn(speed):
    PWM1.duty_u16(int(speed * 65535 / 100)) 
    PWM2.duty_u16(int(speed * 65535 / 100))
    PWM3.duty_u16(int(speed * 65535 / 100))
    PWM4.duty_u16(int(speed * 65535 / 100))


def debug(pin, speed):
    pin.high()
    pwmOn(speed)
#     PWM3.duty_u16(int(speed * 65535 / 100))

def setPower(power1, power2, power3, power4):
    """Set power levels for each motor.
    
    Args:
        power1 (int): Power level for motor 1 (0-100%).
        power2 (int): Power level for motor 2 (0-100%).
        power3 (int): Power level for motor 3 (0-100%).
        power4 (int): Power level for motor 4 (0-100%).
    """
    PWM1.duty_u16(int(power1 * 65535 / 100))
    PWM2.duty_u16(int(power2 * 65535 / 100))
    PWM3.duty_u16(int(power3 * 65535 / 100))
    PWM4.duty_u16(int(power4 * 65535 / 100))

d2.high()
time.sleep(1)
d2.low()
d1.high()
time.sleep(1)


# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SBRT', 'Robotic$3')
# wlan.connect('NETGEAR62', 'luckyoctopus633')
time.sleep(5)

# Wait for connection
max_attempts = 10
attempt = 0

while not wlan.isconnected() and attempt < max_attempts:
    print(f"Trying to connect to (Attempt {attempt + 1}/{max_attempts})...")
    time.sleep(10)
    attempt += 1

if wlan.isconnected():
    print("Connected to IP:", wlan.ifconfig()[0])
    d1.high()
    time.sleep(1)
    d1.low()
    
else:
    print("Failed to connect to Wi-Fi. Please check your SSID and password.")



app = Microdot()
CORS(app, allowed_origins = '*', allow_credentials = True)

@app.get('/test')
def index(requsst):
    return "hello world"

def set_wheel_direction(left_dir, right_dir):
    # Left side wheels
    frontLeft1.value(left_dir[1])
    frontLeft2.value(left_dir[0])
    backLeft1.value(left_dir[1])
    backLeft2.value(left_dir[0])
    
    # Right side wheels
    frontRight1.value(right_dir[1])
    frontRight2.value(right_dir[0])
    backRight1.value(right_dir[1])
    backRight2.value(right_dir[0])


    # Function to control wheel speed using PWM
def motion(left, right):
    print(f"Wheel1: {wheel1}, Wheel2: {wheel2}")

    PWM1.duty_u16(int(left * 65535 / 100))
    PWM2.duty_u16(int(right * 65535 / 100))
#     PWM3.duty_u16(int(wheel1 * 65535 / 100))
#     PWM4.duty_u16(int(wheel2 * 65535 / 100))



def move(x, y):
    print("moving\n")
    
    # Adjust power dynamically based on the turn direction
    if x > 0 and y > 0:  # Forward and turn right (right motors slower)
        print("forward and turn right")
        frontLeft1.high()
        backLeft1.high()
        frontRight1.high()
        backRight1.high()
        PWM1.duty_u16(int(100 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(45 * 65535 / 100)) #pwm2 right
    elif x > 0 and y == 0:
        print("right")
        frontLeft1.high()
        backLeft2.high()
        frontRight1.high()
        backRight2.high()
        PWM1.duty_u16(int(100 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(100 * 65535 / 100)) #pwm2 right
    elif x < 0 and y == 0:
        print("left")
        frontLeft2.high()
        backLeft1.high()
        frontRight2.high()
        backRight1.high()
        PWM1.duty_u16(int(100 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(100 * 65535 / 100)) #pwm2 right
    elif x == 0 and y > 0:
        print("forward")
        frontLeft1.high()
        backLeft1.high()
        frontRight1.high()
        backRight1.high()
        PWM1.duty_u16(int(100 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(100 * 65535 / 100)) #pwm2 right
        
    elif x == 0 and y < 0:
        print("backward")
        frontLeft2.high()
        backLeft2.high()
        frontRight2.high()
        backRight2.high()
        PWM1.duty_u16(int(100 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(100 * 65535 / 100)) #pwm2 right

    elif x < 0 and y < 0:  # Backward and turn left (left motors slower)
        print("backward and turn left")
        frontLeft2.high()
        backLeft2.high()
        frontRight2.high()
        backRight2.high()
        PWM1.duty_u16(int(30 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(100 * 65535 / 100)) #pwm2 right

    elif x > 0 and y < 0:  # Backward and turn right (right motors slower)
        print("backward and turn right")
        frontLeft2.high()
        backLeft2.high()
        frontRight2.high()
        backRight2.high()
        PWM1.duty_u16(int(100 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(30 * 65535 / 100)) #pwm2 right

    elif x < 0 and y > 0:  # Forward and turn left (left motors slower)
        frontLeft1.high()
        backLeft1.high()
        frontRight1.high()
        backRight1.high()
        PWM1.duty_u16(int(45 * 65535 / 100)) #PWM1 left
        PWM2.duty_u16(int(100 * 65535 / 100)) #pwm2 right
    elif x==0 and y==0:
        allOff()

# def testRight(x, y): #forward right
#     if x!= 0 or y != 0:
#         frontLeft1.high()
#         backLeft1.high()
#         frontRight1.high()
#         backRight1.high()
#         PWM1.duty_u16(int(100 * 65535 / 100)) #PWM1 left
#         PWM2.duty_u16(int(45 * 65535 / 100)) #pwm2 right
#     else:
#         allOff()

@app.get('/direction')
@with_websocket
async def index(request, ws): 
    try:
        while True:
            data = await ws.receive()
            if not data:
                break
            try:
                joystick_data = json.loads(data)
                    
                x = joystick_data.get('x', 0)
                y = -1 * joystick_data.get('y', 0)
                print(data)

                print(x, y)
                
                move(x,y)
                

            except Exception as e:
                print(f"no can do: {e}")
            
        
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket connection closed")
        await ws.close()

app.run(port=80)

