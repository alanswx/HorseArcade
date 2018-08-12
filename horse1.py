import pygame
import sys
from PIL import Image
import AnimatedSprite1 as AnimatedSprite
import AnimatedCountdown

try:
    from matrix import MatrixScreen
except ImportError:
    from matrix_null import MatrixScreen

screenpanels_width =  8
screenpanels_height =  2
screenpanel_pixels = 64
screenwidth = screenpanel_pixels * screenpanels_width
screenheight = screenpanel_pixels * screenpanels_height
horseheight = 20
horsewidth = 32
finishlinex = 40
minpeople = 2
grass = pygame.image.load('images/background_2.png')
class Horse:
    def __init__(self, slotnumber):
        self.sprite=AnimatedSprite.AnimatedSprite('images/horse_'+str(slotnumber+1)+'/Horse '+str(slotnumber+1),12)
        self.slotnumber = slotnumber
        self.reset()
        self.hide()
        self.current_time = 0 # for time logging
        self.timerStarted = False
    def hide(self):
        self.hidden = True
    def show(self):
        self.hidden = False
    def reset(self):
        self.x = screenwidth - horsewidth
        self.y = horseheight * self.slotnumber
        self.feet = 0
        self.done = False
        self.hide()
        self.current_time = 0 # for time logging
        self.timerStarted = False
    def draw(self,dt,screen, start):
        if self.hidden:
            return
        if start == True:
            self.timerStarted = True
        if self.timerStarted == True:
            self.current_time += dt # for time logging
        if start == True and self.slotnumber == 0:
            screen.blit(still0, [self.x,self.y])
        if start == True and self.slotnumber == 1:
            screen.blit(still1, [self.x,self.y])
        if start == True and self.slotnumber == 2:
            screen.blit(still2, [self.x,self.y])
        if start == True and self.slotnumber == 3:
            screen.blit(still3, [self.x,self.y])
        if start == False:
            self.sprite.update(dt,screen,self.x,self.y)
            if self.x <= finishlinex:
                self.done = True
    def done(self):
        return self.done
    def button(self, paw):
        if self.hidden:
            return
        if self.x > finishlinex:
            if self.feet == 0:
              if paw == 0:
               self.x=self.x-horsewidth//4
               self.feet=1
            if self.feet == 1:
              if paw == 1:
               self.x=self.x-horsewidth//4
               self.feet=0
        elif self.x < finishlinex:
            self.timerStarted = False

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Start(States):
    def __init__(self, app):
        self.sprite=AnimatedCountdown.AnimatedSprite('images/countdown',6, 5)
        self.app = app
        States.__init__(self)
        self.next = 'game'
        self.numpeople = 0
    def startup(self):
        self.timerStarted = False
        self.time = 6
        for horse in self.app.horses:
            horse.reset()
        self.numpeople = 0
        print('starting Start state')
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                if self.app.horses[0].hidden:
                    self.numpeople += 1
                    print('Player 0 joined')
                    print('There are '+str(self.numpeople)+' people ready')
                self.app.horses[0].show()
            if event.key == pygame.K_e:
                if self.app.horses[1].hidden:
                    self.numpeople += 1
                    print('Player 1 joined')
                    print('There are '+str(self.numpeople)+' people ready')
                self.app.horses[1].show()
            if event.key == pygame.K_d:
                if self.app.horses[2].hidden:
                    self.numpeople += 1
                    print('Player 2 joined')
                    print('There are '+str(self.numpeople)+' people ready')
                self.app.horses[2].show()
            if event.key == pygame.K_c:
                if self.app.horses[3].hidden:
                    self.numpeople += 1
                    print('Player 3 joined')
                    print('There are '+str(self.numpeople)+' people ready')
                self.app.horses[3].show()
        if self.numpeople >= minpeople:
                self.timerStarted = True
    def update(self, screen, dt):
        self.draw(screen, dt)
        if self.timerStarted == True:
            self.time = self.time - dt
        if self.time < 0 and self.timerStarted == True:
            self.done = True
    def draw(self, screen, dt):
        screen.blit(grass, [0,0])
        if self.timerStarted == False:
            screen.blit(grass, [0,0])
            title_rect = title.get_rect()
            title_rect.centerx = 256
            title_rect.centery = 64
            screen.blit(title, title_rect)
        if self.timerStarted == True:
            self.sprite.update(dt, screen)
        for horse in self.app.horses:
            horse.draw(dt, screen, True)
class Game(States):
    def __init__(self, app):
        self.sprite=AnimatedCountdown.AnimatedSprite('images/countdownend', 5, 4)
        self.app = app
        States.__init__(self)
        self.next = 'finish'
    def startup(self):
        self.timerStarted = False
        self.time = 5
        print('starting Game state')
    def get_event(self, event):
          if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_1:
                  self.app.horses[0].button(0)
               if event.key == pygame.K_2:
                  self.app.horses[0].button(1)
               if event.key == pygame.K_q:
                  self.app.horses[1].button(0)
               if event.key == pygame.K_w:
                  self.app.horses[1].button(1)
               if event.key == pygame.K_a:
                  self.app.horses[2].button(0)
               if event.key == pygame.K_s:
                  self.app.horses[2].button(1)
               if event.key == pygame.K_z:
                  self.app.horses[3].button(0)
               if event.key == pygame.K_x:
                  self.app.horses[3].button(1)
    def update(self, screen, dt):
        self.draw(screen, dt)
        if self.timerStarted == True:
            self.time = self.time - dt
        if self.time < 0 and self.timerStarted == True:
            self.done = True
    def draw(self, screen, dt):
        screen.blit(grass, [0,0])
        for horse in self.app.horses:
            horse.draw(dt, screen, False)
            if horse.done:
                self.timerStarted = True
        if self.timerStarted == True:
            self.sprite.update1(dt, screen)

class Finish(States):
    def __init__(self, app):
        self.app = app
        States.__init__(self)
        self.next = 'start'
    def startup(self):
        print('starting Finish state')
        for horse in self.app.horses:
            print(str(horse.slotnumber+1)+': ' + str(horse.current_time)) #printing timings
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
        self.horses = []
        self.horses.append(Horse(0))
        self.horses.append(Horse(1))
        self.horses.append(Horse(2))
        self.horses.append(Horse(3))
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()
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
            surface = pygame.display.get_surface()
            data = pygame.image.tostring(surface,'RGB')
            img = Image.frombytes('RGB',(screenwidth,screenheight),data)
            matrix.draw(img)
            pygame.display.update()

settings = {
    'size':(screenwidth,screenheight),
    'fps' :60
}

app = Control(**settings)
state_dict = {
    'start': Start(app),
    'game': Game(app),
    'finish':Finish(app)
}
pygame.init()
matrix = MatrixScreen()
title = pygame.image.load('title.png').convert_alpha()
winner = pygame.image.load('winner.png').convert_alpha()
still0 = pygame.image.load('images/horses_still/Horse 01.png')
still1 = pygame.image.load('images/horses_still/Horse 02.png')
still2 = pygame.image.load('images/horses_still/Horse 03.png')
still3 = pygame.image.load('images/horses_still/Horse 04.png')
app.setup_states(state_dict, 'start')
app.main_game_loop()
pygame.quit()
sys.exit()
