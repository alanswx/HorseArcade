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
pwm = Adafruit_PCA9685.PCA9685()
def dispense_init():
    pwm.set_pwm_freq(60)
    servo_min = config.servo_min
    servo_max = config.servo_max
    pwm.set_pwm(0, 0, servo_max)
    pwm.set_pwm(1, 0, servo_max)
    pwm.set_pwm(2, 0, servo_max)
    pwm.set_pwm(3, 0, servo_max)
    print("Initializing servo")
def dispense_back(channel):
    # Move servo on channel O between extremes.
    pwm.set_pwm(channel, 0, servo_min)
    print("Dispenser " + str(channel+1)+": Pulling Back")
def dispense_forward(channel):
    pwm.set_pwm(channel, 0, servo_max)
    time.sleep(1)
    print("Dispenser " + str(channel+1)+": Dispensing Candy")
