BOARD = 1
OUT = 1
IN = 1
BCM = 1

def setmode(a):
   print ('GPIO.setmode:',a)
def setup(a, b):
   print ('GPIO.setup:',a)
def output(a, b):
   print ('GPIO.output:',a)
def cleanup():
   print ('GPIO.cleanup')
def setwarnings(flag):
   print ('GPIO.setwarnings:',flag)
