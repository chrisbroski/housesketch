import time
import RPi.GPIO as GPIO
break_pin = 27
led_pin = 17

try:
    GPIO.cleanup()
except:
    print('no cleanup')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(break_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, False)

while True:
    print(GPIO.input(break_pin))
    if GPIO.input(break_pin):
        # led on
        GPIO.output(led_pin, False)
    else:
        # led off
        GPIO.output(led_pin, True)
    
    time.sleep(0.1)
