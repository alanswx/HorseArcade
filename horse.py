#!/usr/bin/env python

from PIL import Image
import pygame


screenpanels_width =  8 
screenpanels_height =  2 
screenpanel_pixels = 64
screenwidth = screenpanel_pixels * screenpanels_width
screenheight = screenpanel_pixels * screenpanels_height

horsepos = screenwidth - 32
horseheight = 32
#
#   create a sprite class for each horse
#

class Horse:
    def __init__(self, slotnumber):
        self.x = horsepos
        self.y = horseheight * slotnumber
        self.feet =  0
        #self.


# init
# draw
# button


#
#  create a horse track (background)
#


#
#  main loop
#

#  - read the keys
#  - move sprites
#  - draw the sprites to the offscreen buffer
#  - swap the buffers
# -- if RGB Matrix - we will draw there, otherwise use pygame

 
grass = Image.open("grass.png")
mode = grass.mode
size = grass.size
data = grass.tobytes()
grass_image = pygame.image.fromstring(data, size, mode)

image = Image.open("horse.png")
mode = image.mode
size = image.size
data = image.tobytes()

this_image = pygame.image.fromstring(data, size, mode)

#this_image = pygame.image.load("animated-horse-gif-11.gif").convert()


pygame.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
done = False

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_LEFT:
                        horsepos-=32

        #pygame.draw.rect(screen, (0,100,0),(0,0,screenwidth,screenheight),0)
        screen.blit(grass_image,(0,0))
        screen.blit(this_image,(horsepos,0))
        pygame.display.flip()
