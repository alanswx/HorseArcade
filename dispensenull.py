import time
import logging

def dispense_init():
    logging.debug("Initializing servo")
def dispense_back(channel = None):
    logging.debug("Dispenser " + str(channel+1)+": Pulling Back")
def dispense_forward(channel = None):
    logging.debug("Dispenser " + str(channel+1)+": Dispensing Candy")

if __name__ == "__main__":
    for i in range(42):
        dispense_back(0)
        dispense_back(1)
        dispense_back(2)
        dispense_back(3)
        time.sleep(2)
        dispense_forward(0)
        dispense_forward(1)
        dispense_forward(2)
        dispense_forward(3)
        time.sleep(2)
