import RPi.GPIO as GPIO
import time, sys, os
import subprocess
from subprocess import Popen
from pathlib import Path
from time import sleep

actions = {
    'pulse': {
        'duration': 3
    },
    'shh': {
        'video': 'siloMaleV3.mov',
        'duration': 5
    },
    'alarm sequence': {
        'duration': 8
    },
    'music and sillouettes': {
        'duration': 5
    }
}

# clean-up was getting an error message so I commented it out
#try:
 #   GPIO.cleanup()
#except:
 #   print('nothing to clean')

print("Start house sketch")

# Set pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_TRIGECHO = 15
break_pin = 27
#GPIO.setup(GPIO_TRIGECHO,GPIO.OUT)
#GPIO.setup(break_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.output(GPIO_TRIGECHO, False)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.OUT)

distance = 200

def measure():
    return 1000
    #GPIO.output(GPIO_TRIGECHO, True)
    #time.sleep(0.00001)
    #GPIO.output(GPIO_TRIGECHO, False)

    #start = time.time()

    # set line to input to check for start of echo response
    #GPIO.setup(GPIO_TRIGECHO, GPIO.IN)
    #while GPIO.input(GPIO_TRIGECHO)==0:
    #    start = time.time()

    # Wait for end of echo response
    #while GPIO.input(GPIO_TRIGECHO)==1:
    #    stop = time.time()

    #GPIO.setup(GPIO_TRIGECHO, GPIO.OUT)
    #GPIO.output(GPIO_TRIGECHO, False)

    #elapsed = stop-start
    #distance = (elapsed * 34300)/2.0
    #return distance

def take_action(act):
    print(act)

    if 'video' in actions[act]:
        subprocess.Popen('omxplayer ' + str(Path(actions[act]['video'])), shell=True)
    
    if 'duration' in actions[act]:
        sleep(actions[act]['duration'])

def sense():
    #if not GPIO.input(break_pin):
    #    take_action('alarm sequence')
    #    return

    global distance
    distance = (measure() + distance) / 2

    if distance <= 61:
        take_action('shh')
        #subprocess.call('pkill -9 omxplayer', shell=true)
        return

    if distance <= 183:
        take_action('music and sillouettes')
        return
    
    if GPIO.input(23) == False:
        take_action('shh')

    take_action('pulse')

try:
    while True:
        sense()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stop")
    GPIO.cleanup()
