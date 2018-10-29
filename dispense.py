import time
import logging

try:
  import config
except ImportError:
    print ("no config.py found.  Please copy sample_config.py to config.py.")

# Import the PCA9685 module.
import Adafruit_PCA9685

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Set frequency to 60hz, good for servos.
pwm = Adafruit_PCA9685.PCA9685()

def dispense_init():
    pwm.set_pwm_freq(60)
    logging.debug("Initializing servo")

def dispense_back(channel):
    pwm.set_pwm(channel, 0, config.servo_max)
    logging.debug("Dispenser " + str(channel+1)+": Pulling Back")

def dispense_forward(channel):
    pwm.set_pwm(channel, 0, config.servo_min)
    logging.debug("Dispenser " + str(channel+1)+": Dispensing Candy")
