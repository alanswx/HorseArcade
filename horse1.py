import pygame as pygame
import sys
from PIL import Image
import AnimatedSprite1 as AnimatedSprite
screenpanels_width =  8
screenpanels_height =  2
screenpanel_pixels = 64
screenwidth = screenpanel_pixels * screenpanels_width
screenheight = screenpanel_pixels * screenpanels_height
horseheight = 20
horsewidth = 32
finishlinex = 40
grass = pygame.image.load('grass.png')
class Horse:
    def __init__(self, slotnumber):
        self.sprite=AnimatedSprite.AnimatedSprite('images/horse_0/horse_'+str(0),12)
        self.slotnumber = slotnumber
        self.reset()
    def reset(self):
        self.x = screenwidth - horsewidth
        self.y = horseheight * self.slotnumber
        self.feet = 0
        self.done = False
    def draw(self,dt,screen):
        self.sprite.update(dt,screen,self.x,self.y)
        if self.x <= finishlinex:
            self.done = True
    def done(self):
        return self.done
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

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Start(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
    def startup(self):
        print('starting Start state')
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.blit(grass, [0,0])
        title_rect = title.get_rect()
        title_rect.centerx = 256
        title_rect.centery = 64
        screen.blit(title, title_rect)

class Game(States):
    def __init__(self):
        self.horses = []
        self.horses.append(Horse(0))
        self.horses.append(Horse(1))
        self.horses.append(Horse(2))
        self.horses.append(Horse(3))
        States.__init__(self)
        self.next = 'finish'
    def startup(self):
        print('starting Game state')
        for horse in self.horses:
            horse.reset()
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_1:
                self.horses[0].button(0)
             if event.key == pygame.K_2:
                self.horses[0].button(1)
             if event.key == pygame.K_q:
                self.horses[1].button(0)
             if event.key == pygame.K_w:
                self.horses[1].button(1)
             if event.key == pygame.K_a:
                self.horses[2].button(0)
             if event.key == pygame.K_s:
                self.horses[2].button(1)
             if event.key == pygame.K_z:
                self.horses[3].button(0)
             if event.key == pygame.K_x:
                self.horses[3].button(1)
    def update(self, screen, dt):
        self.draw(screen, dt)
    def draw(self, screen, dt):
        screen.blit(grass, [0,0])
        for horse in self.horses:
            horse.draw(dt, screen)
            if horse.done:
                self.done = True

class Finish(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'start'
    def startup(self):
        print('starting Finish state')
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.blit(grass, [0,0])
        winner_rect = winner.get_rect()
        winner_rect.centerx = 256
        winner_rect.centery = 64
        screen.blit(winner, winner_rect)
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            #self.screen = pygame.transform.scale(self.screen, (screenwidth*2, screenheight*2))
            pygame.display.update()

settings = {
    'size':(screenwidth,screenheight),
    'fps' :60
}

app = Control(**settings)
state_dict = {
    'start': Start(),
    'game': Game(),
    'finish':Finish()
}
pygame.init()
title = pygame.image.load('title.png').convert_alpha()
winner = pygame.image.load('winner.png').convert_alpha()
app.setup_states(state_dict, 'start')
app.main_game_loop()
pygame.quit()
sys.exit()
