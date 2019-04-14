# coding: utf-8
import time
import RPi.GPIO as GPIO

try:
    GPIO.cleanup()
except:
    print('nothing to clean')
    
GPIO.setwarnings(False)
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGECHO = 15
break_pin = 27

current_action = 'pulse'
sequence_time = 10000
distance = 200

print("Ultrasonic Measurement")

# Set pins as output and input
GPIO.setup(GPIO_TRIGECHO,GPIO.OUT)  # Initial state as output
GPIO.setup(break_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGECHO, False)

def measure():
  # This function measures a distance
  # Pulse the trigger/echo line to initiate a measurement
    GPIO.output(GPIO_TRIGECHO, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGECHO, False)
  #ensure start time is set in case of very quick return
    start = time.time()

  # set line to input to check for start of echo response
    GPIO.setup(GPIO_TRIGECHO, GPIO.IN)
    while GPIO.input(GPIO_TRIGECHO)==0:
        start = time.time()

  # Wait for end of echo response
    while GPIO.input(GPIO_TRIGECHO)==1:
        stop = time.time()

    GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
    GPIO.output(GPIO_TRIGECHO, False)

    elapsed = stop-start
    distance = (elapsed * 34300)/2.0
    return distance

def take_action(act):
    current_action = act
    print(act)

def sense():
    if sequence_time < 10000:
        return

    if not GPIO.input(break_pin):
        take_action('alarm sequence')
        return

    global distance
    distance = (measure() + distance) / 2
    # print("  Distance : %.1f cm" % distance)

    if distance <= 61:
        take_action('shh')
        return

    if distance <= 183:
        take_action('music and sillouettes')
        return

    take_action('pulse')

try:

    while True:

        #distance = measure()
        #print("  Distance : %.1f cm" % distance)
        sense()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stop")
    GPIO.cleanup()
