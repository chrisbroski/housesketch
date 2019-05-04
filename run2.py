import RPi.GPIO as GPIO
import time, sys, os
import time
import subprocess
from subprocess import Popen
from pathlib import Path
from time import sleep

actions = {
    'pulse': {
        'video': 'Pulse.mov',
        'duration': 20
    },
    'shh': {
        'video': 'siloMaleV3.mov',
        'duration': 3
    },
    'alarm': {
        'video': 'SirenV1.mov',
        'duration': 10
    },
    'music and sillouettes': {
        'video': 'PartyV1.mov',
        'duration': 8
    }
}

GPIO.setwarnings(False)

# clean-up was getting an error message so I commented it out
#try:
#    GPIO.cleanup()
#except:
#    print('nothing to clean')
 
current_action = ''
new_action = ''
new_action_count = 0
action_time = time.time()

GPIO.setmode(GPIO.BCM)
GPIO_TRIGECHO = 15
break_pin = 27
GPIO.setup(GPIO_TRIGECHO,GPIO.OUT)
GPIO.setup(break_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(GPIO_TRIGECHO, False)

distance = 200

def measure():
    GPIO.output(GPIO_TRIGECHO, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGECHO, False)
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
    global current_action
    global new_action
    global new_action_count
    global action_time
    start = False
    
    if act != current_action:
        if act != new_action:
            new_action = act
            new_action_count = 0
        else:
            new_action_count += 1

    if current_action == '':
        current_action = act
        start = True

    if current_action == 'alarm' and time.time() < action_time + actions[current_action]['duration']:
        return

    if new_action_count > 3:
        current_action = new_action
        new_action_count = 0
        start = True
    
    if act == 'alarm' and current_action != 'alarm':
        current_action = 'alarm'
        new_action_count = 0
        start = True
    
    if start:
        print('starting', current_action)
        action_time = time.time()
        #subprocess.Popen('omxplayer ' + str(Path(actions[current_action]['video'])), shell=True)
    
    if time.time() > action_time + actions[current_action]['duration']:
        #subprocess.Popen('omxplayer ' + str(Path(actions[current_action]['video'])), shell=True)
        if current_action == 'alarm':
            current_action = act
        print('re-starting', current_action)
        action_time = time.time()


def sense():
    if not GPIO.input(break_pin):
        take_action('alarm')
        return

    global distance
    distance = measure()

    if distance <= 61:
        take_action('shh')
        return

    if distance <= 183:
        take_action('music and sillouettes')
        return

    take_action('pulse')


try:
    while True:
        sense()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stop")
    GPIO.cleanup()

