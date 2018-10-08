# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
try:
  import config
except ImportError:
    print ("no config.py found.  Please copy sample_config.py to config.py.")

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).


# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Set frequency to 60hz, good for servos.
def dispense_init():
    pwm.set_pwm_freq(60)
    pwm = Adafruit_PCA9685.PCA9685()
    servo_min = config.servo_min
    servo_max = config.servo_max
    pwm.set_pwm(channel, 0, servo_min)
    print("Initializing servo")
def dispense_back(channel):
    # Move servo on channel O between extremes.
    pwm.set_pwm(channel, 0, servo_min)
    print("Dispenser " + str(channel+1)+": Pulling Back")
def dispense_forward(channel):
    pwm.set_pwm(channel, 0, servo_max)
    time.sleep(1)
    print("Dispenser " + str(channel+1)+": Dispensing Candy")
"""print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on channel O between extremes.
    while 1:
        pwm.set_pwm(0, 0, servo_min)
        d = raw_input("Ready for %d:" % servo_min)
        d = d.strip()
        try:
            d = int(d)
            if d:
                servo_min = d
        except ValueError:
            pass
        print (repr(d))
        if d == "": break

    while 1:
        pwm.set_pwm(0, 0, servo_max)
        d = raw_input("Ready for %d:" % servo_max)
        d = d.strip()
        try:
            d = int(d)
            if d:
                servo_max = d
        except ValueError:
            pass

        if d == "": break """
