import RPi.GPIO as GPIO
import subprocess
from subprocess import Popen
from pathlib import Path
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.OUT)

timer = 0
vid1_length = 3

try:
    while True:
        button_state = GPIO.input(23)
        if button_state == False:
            GPIO.output(21, True)
            if time.time() > timer + vid1_length:
                timer = time.time()
                Popen('omxplayer ' + str(Path("siloMaleV3.mov")), shell=True)
        else:
            GPIO.output(21, False)
except Exception as e:
    print(str(e))
    GPIO.cleanup()
