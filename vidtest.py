import RPi.GPIO as GPIO
import time, sys, os
import subprocess
from subprocess import Popen


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.OUT)

try:
    while True:
        button_state = GPIO.input(23)
        if button_state == False:
            print('pressed')
            GPIO.output(21, True)
            Popen('omxplayer /home/pi/repos/housesketch/siloMaleV3.mov', shell=True)
        else:
            GPIO.output(21, False)
except:
    GPIO.cleanup()
