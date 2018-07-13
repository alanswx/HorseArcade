#!/usr/bin/env python

from PIL import Image
import pygame

import AnimatedSprite


screenpanels_width =  8
screenpanels_height =  2
screenpanel_pixels = 64
screenwidth = screenpanel_pixels * screenpanels_width
screenheight = screenpanel_pixels * screenpanels_height
horseheight = 20
horsewidth = 32
finishlinex = 40
finish = False


screen = Image.new('RGB', (screenwidth,screenheight))


grass = Image.open("grass.png")
horse = Image.open("horse.png")



#
#   create a sprite class for each horse
#horse
class Horse:
    def __init__(self, slotnumber):
        self.sprite=AnimatedSprite.AnimatedSprite('images/horse_0/horse_'+str(0),12)
        self.x = screenwidth - horsewidth
        self.y = horseheight * slotnumber
        self.feet = 0
    def draw(self,dt):
        self.sprite.update(dt,screen,self.x,self.y)
        #screen.paste(horse, (self.x, self.y), horse)
    def button(self, paw):
        if self.x > finishlinex:
            if self.feet == 0:
              if paw == 0:
               self.x=self.x-horsewidth//4
               self.feet=1
            if self.feet == 1:
              if paw == 1:
               self.x=self.x-horsewidth//4
               self.feet=0
        else:
          finish = True
# init
# draw
# button

horses = []
horses.append(Horse(0))
horses.append(Horse(1))
horses.append(Horse(2))
horses.append(Horse(3))


#
#  create a horse track (background)
#
def drawGame(dt):
    screen.paste(grass)
    for horse in horses:
        horse.draw(dt)
    return screen

#
#  main loop
#

#  - read the keys
#  - move sprites
#  - draw the sprites to the offscreen buffer
#  - swap the buffers
# -- if RGB Matrix - we will draw there, otherwise use pygame

#this_image = pygame.image.load("animated-horse-gif-11.gif").convert()

FPS = 60
clock = pygame.time.Clock()

pygame.init()
screen_pygame = pygame.display.set_mode((screenwidth * 2, screenheight * 2), 0, 24)
screen_2x = pygame.Surface((screenwidth*2,screenheight*2), 0 , 24)
done = False

while not done:
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_1:
                        horses[0].button(0)
                     if event.key == pygame.K_2:
                        horses[0].button(1)
                     if event.key == pygame.K_q:
                        horses[1].button(0)
                     if event.key == pygame.K_w:
                        horses[1].button(1)
                     if event.key == pygame.K_a:
                        horses[2].button(0)
                     if event.key == pygame.K_s:
                        horses[2].button(1)
                     if event.key == pygame.K_z:
                        horses[3].button(0)
                     if event.key == pygame.K_x:
                        horses[3].button(1)

        #pygame.draw.rect(screen, (0,100,0),(0,0,screenwidth,screenheight),0)
        screen = drawGame(dt)
        mode = screen.mode
        size = screen.size
        data = screen.tobytes()
        screen_image = pygame.image.fromstring(data, size, mode)
        #screen_pygame.blit(screen_image,(0,0))
        pygame.transform.scale2x(screen_image, screen_2x)
        screen_pygame.blit(screen_2x,(0,0))
        pygame.display.flip()
