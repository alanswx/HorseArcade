import pygame

BOARD = 1
OUT = 1
IN = 1
BCM = 1
gpiosurface = None

def setmode(a):
   print ('GPIO.setmode:',a)
def setup(a, b):
   print ('GPIO.setup:',a)
def output(a, b):
   print ('GPIO.output:',a,b)
   p = (a*20,200)
   if (gpiosurface!=None):
       pygame.draw.circle(gpiosurface, (249,8,28), p,10)
       if (b==0):
          pygame.draw.circle(gpiosurface, (10,10,10), p,8)
   else:
       print('no gpio surface')
def cleanup():
   print ('GPIO.cleanup')
def setwarnings(flag):
   print ('GPIO.setwarnings:',flag)
def setsurface(surface):
    print('set surface')
    global gpiosurface
    gpiosurface=surface
