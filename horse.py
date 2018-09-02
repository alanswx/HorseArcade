import pygame
import sys
from PIL import Image
import AnimatedSprite

try:
    from mf import MatrixScreen
except ImportError:
    from matrix_null import MatrixScreen
#from matrix_null import MatrixScreen

screenpanels_width =  8
screenpanels_height =  2
screenpanel_pixels = 64
screenwidth = screenpanel_pixels * screenpanels_width
screenheight = screenpanel_pixels * screenpanels_height
horseheight = 20
horsewidth = 32
finishlinex = 40
minpeople = 2
SONG_END = pygame.USEREVENT + 1

grass = pygame.image.load('images/background_2.png')
class Horse:
    def __init__(self, slotnumber):
        self.sprite=AnimatedSprite.AnimatedSprite('images/horse_'+str(slotnumber+1)+'/Horse '+str(slotnumber+1)+'-',12)
        self.still = pygame.image.load('images/horses_still/Horse 0'+str(slotnumber +1)+'.png')
        self.slotnumber = slotnumber
        self.character = pygame.image.load('images/horse_'+str(self.slotnumber + 1)+'/Horse Character '+str(self.slotnumber + 1) +'.png').convert_alpha()
        self.reset()
        self.hide()
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
    def reset_time(self):
        self.startTime = pygame.time.get_ticks() # for time logging
        self.endTime = pygame.time.get_ticks()
    def draw(self,dt,screen, start):
        if self.hidden:
            return
        if start == True or self.done == True:
            screen.blit(self.still, [self.x,self.y])
        elif start == False:
            self.sprite.update(dt,screen,self.x,self.y)
            if self.x <= finishlinex:
                self.done = True
                self.endTime = pygame.time.get_ticks()
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
        self.sprite=AnimatedSprite.AnimatedSprite('images/countdown',6, 5,offset=-1,animation_time=1)
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
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            print(event)
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
                if self.timerStarted==False:
                    pygame.mixer.music.load('sounds/racestart.ogg')
                    pygame.mixer.music.set_endevent(SONG_END)

                    pygame.mixer.music.play(0)
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
        self.sprite=AnimatedSprite.AnimatedSprite('images/countdownend', 5, 4, pygame.image.load('images/endgame.png').convert_alpha(),offset=-1,animation_time=1)
        self.app = app
        States.__init__(self)
        self.next = 'finish'
    def startup(self):
        self.timerStarted = False
        self.time = 5
        for horse in self.app.horses:
            horse.reset_time()
        print('starting Game state')

    def get_event(self, event):
          if event.type == SONG_END:
            print("the song ended!")
            pygame.mixer.music.load('sounds/horsesounds.ogg')
            pygame.mixer.music.play(0)

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
            self.sprite.update(dt, screen)
class Finish(States):
    def __init__(self, app):
        self.app = app
        States.__init__(self)
        self.next = 'start'
    def startup(self):
        print('starting Finish state')
        pygame.mixer.music.load('sounds/finish.ogg')
        pygame.mixer.music.play(0)
        for horse in self.app.horses:
            print(str(horse.slotnumber+1)+': '+str((horse.endTime-horse.startTime)/1000)) #printing timings
            if horse.endTime - horse.startTime == 0:
                horse.endTime = horse.startTime+9999999
        self.sortedlist = self.app.horses.copy()
        self.sortedList=sorted(self.sortedlist, key=lambda horse: (horse.endTime,horse.x))
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.blit(results, [0,0])
        for col in range(2):
            for row in range(2):
                horse=self.sortedList[col*2+row]
                if not horse.hidden:
                    #print((col,row))
                    #print(str(horse.slotnumber+1)+': '+str((horse.endTime-horse.startTime)/1000)+' '+str(horse.x))
                    horsecharacter = horse.character
                    horsecharacter_rect = horsecharacter.get_rect()
                    horsecharacter_rect.x = ((col) * 256) + 40
                    horsecharacter_rect.y = ((row) * 24) + 64
                    screen.blit(horsecharacter, horsecharacter_rect)
                    myfont = pygame.font.SysFont('Comic Sans MS', 30)
                    textsurface = myfont.render(str(horse.endTime-horse.startTime/1000), True, (255,255,255))
                    screen.blit(textsurface, (horsecharacter_rect.x + 64, horsecharacter_rect.y))
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.horses = []
        for horsenum in range(4):
            self.horses.append(Horse(horsenum))
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
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

matrix = MatrixScreen()
title = pygame.image.load('images/title.png').convert_alpha()
results = pygame.image.load('images/results.png').convert_alpha()
app.setup_states(state_dict, 'start')
app.main_game_loop()
pygame.quit()
sys.exit()
