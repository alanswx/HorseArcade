#! /usr/bin/env python3

import os, sys, string, time, logging, argparse

import pygame
from PIL import Image
import AnimatedSprite

import config

x = 0
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#try:
#    from mf import MatrixScreen
#except ImportError:
#    from matrix_null import MatrixScreen
from matrix_null import MatrixScreen

SONG_END = pygame.USEREVENT + 1

class Horse:
    def __init__(self, slotnumber, name):
        self.name = name
        self.slotnumber = slotnumber

        self.sprite = AnimatedSprite.AnimatedSprite(os.path.join(config.imagePath, 'horse_%d' % (slotnumber+1), 'Horse %d-' % (slotnumber+1)),12)
        self.still = pygame.image.load(os.path.join(config.imagePath, 'horses_still', 'Horse 0%d.png' % (slotnumber+1)))
        self.character = pygame.image.load(os.path.join(config.imagePath, 'horse_%d' % (slotnumber+1), 'Horse Character %d.png' % (slotnumber+1))).convert_alpha()
        self.reset()
        self.hide()

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def reset(self):
        self.x = config.tracksize[0] - config.horsesize[0]
        self.y = config.horsesize[1] * self.slotnumber
        self.feet = 0
        self.done = False
        self.hide()

    def reset_time(self):
        self.startTime = pygame.time.get_ticks() # for time logging
        self.endTime = pygame.time.get_ticks()

    def draw(self,dt,screen, numpeople):
        if self.hidden:
            return
        if numpeople >= 2 or self.done == True:
            screen.blit(self.still, [self.x,self.y])
        elif numpeople == -1:
            self.sprite.update(dt,screen,self.x,self.y)
            if self.x <= config.finishlinex:
                self.done = True
                self.endTime = pygame.time.get_ticks()

    def button(self, paw):
        if self.hidden:
            return
        if self.x > config.finishlinex:
            if self.feet == 0:
              if paw == 0:
                self.x=self.x-config.horsesize[0]//4
                self.feet=1
            elif self.feet == 1:
              if paw == 1:
                self.x=self.x-config.horsesize[0]//4
                self.feet=0
        elif self.x < config.finishlinex:
            self.timerStarted = False

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Start(States):
    def __init__(self, app):
        self.sprite=AnimatedSprite.AnimatedSprite(os.path.join(config.imagePath, 'countdown'),6, 5,offset=-1,animation_time=1)
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
        logging.debug('starting Start state')

    def addHorse(self, horseid):
      if self.app.horses[horseid].hidden:
        self.numpeople += 1
        logging.debug('Player %d joined' % horseid)
        logging.debug('There are '+str(self.numpeople)+' people ready')
      self.app.horses[horseid].show()

    def get_event(self, event):
        if event.type == pygame.JOYBUTTONUP:
            logging.debug("Joystick button released.")
            logging.debug(event)
            if event.button==0: self.addHorse(0)
            elif event.button==2: self.addHorse(1)
            elif event.button==4: self.addHorse(2)
            elif event.button==6: self.addHorse(3)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: self.quit = True
            elif event.key == pygame.K_3: self.addHorse(0)
            elif event.key == pygame.K_e: self.addHorse(1)
            elif event.key == pygame.K_d: self.addHorse(2)
            elif event.key == pygame.K_c: self.addHorse(3)

        if self.numpeople >= config.minpeople:
          if self.timerStarted==False:
            pygame.mixer.music.load(os.path.join(config.soundPath, 'racestart.ogg'))
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
        screen.blit(self.app.grass, [0,0])
        if self.timerStarted == False:
            screen.blit(self.app.title, [0,0])
        if self.timerStarted == True:
            self.sprite.update(dt, screen)
        for horse in self.app.horses:
            horse.draw(dt, screen, self.numpeople)

class Game(States):
    def __init__(self, app):
        self.sprite = AnimatedSprite.AnimatedSprite(os.path.join(config.imagePath, 'countdownend'), 5, 4, 
                                                    pygame.image.load(os.path.join(config.imagePath, 'endgame.png')).convert_alpha(),
                                                    offset=-1,animation_time=1)
        self.app = app
        States.__init__(self)
        self.next = 'finish'
    def startup(self):
        self.timerStarted = False
        self.time = 5
        for horse in self.app.horses:
            horse.reset_time()
        logging.debug('starting Game state')

    def get_event(self, event):
          if event.type == SONG_END:
            logging.debug("the song ended!")
            pygame.mixer.music.load(os.path.join(config.soundPath, 'horsesounds.ogg'))
            pygame.mixer.music.play(0)

          if event.type == pygame.JOYBUTTONUP:
            logging.debug("Joystick button released.")
            logging.debug(event)
            if   event.button==0: self.app.horses[0].button(0)
            elif event.button==1: self.app.horses[0].button(1)
            elif event.button==2: self.app.horses[1].button(0)
            elif event.button==3: self.app.horses[1].button(1)
            elif event.button==4: self.app.horses[2].button(0)
            elif event.button==5: self.app.horses[2].button(1)
            elif event.button==6: self.app.horses[3].button(0)
            elif event.button==7: self.app.horses[3].button(1)
          elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_1: self.app.horses[0].button(0)
            elif event.key == pygame.K_2: self.app.horses[0].button(1)
            elif event.key == pygame.K_q: self.app.horses[1].button(0)
            elif event.key == pygame.K_w: self.app.horses[1].button(1)
            elif event.key == pygame.K_a: self.app.horses[2].button(0)
            elif event.key == pygame.K_s: self.app.horses[2].button(1)
            elif event.key == pygame.K_z: self.app.horses[3].button(0)
            elif event.key == pygame.K_x: self.app.horses[3].button(1)
            elif event.key == pygame.K_ESCAPE:
              self.quit = True

    def update(self, screen, dt):
        self.draw(screen, dt)
        if self.timerStarted == True:
            self.time = self.time - dt
        if self.time < 0 and self.timerStarted == True:
            self.done = True

    def draw(self, screen, dt):
        screen.blit(self.app.grass, [0,0])
        for horse in self.app.horses:
            horse.draw(dt, screen, -1)
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
        logging.debug('starting Finish state')
        pygame.mixer.music.load(os.path.join(config.soundPath, 'finish.ogg'))
        pygame.mixer.music.play(0)
        for horse in self.app.horses:
          dt = horse.endTime - horse.startTime
          logging.info("%d: %.3f" % ((horse.slotnumber+1), dt))
          if dt == 0:
            horse.endTime = None
        self.sortedlist = self.app.horses.copy()
        self.sortedList = sorted(self.sortedlist, key=lambda horse: (horse.endTime == None, horse.endTime, horse.x))

    def get_event(self, event):
        if event.type == pygame.JOYBUTTONUP:
          logging.debug("Joystick button released.")
          logging.debug(event)
          if event.button in (0,2,4,6):
            self.done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.done = True
        elif event.type == pygame.KEYDOWN:
          if event.key in (pygame.K_1, pygame.K_q, pygame.K_a, pygame.K_z): self.done = True
          elif event.key == pygame.K_ESCAPE: self.quit = True
                  
    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.app.results, [0,0])
        for col in range(2):
            for row in range(2):
                horse=self.sortedList[col*2+row]
                if not horse.hidden:
                    #logging.debug((col,row))
                    #logging.debug(str(horse.slotnumber+1)+': '+str((horse.endTime-horse.startTime)/1000)+' '+str(horse.x))
                    horsecharacter = horse.character
                    horsecharacter_rect = horsecharacter.get_rect()
                    horsecharacter_rect.x = ((col) * 256) + 40
                    horsecharacter_rect.y = ((row) * 32) + 56
                    screen.blit(horsecharacter, horsecharacter_rect)
                    myfont = pygame.font.SysFont(os.path.join(config.fontPath, 'Bebas Neue.ttf'), 20)
                    textsurface = myfont.render(str(horse.name), True, (255,255,255))
                    screen.blit(textsurface, (horsecharacter_rect.x + 48, horsecharacter_rect.y+8))
                    if horse.endTime is None:
                        textsurface = myfont.render('DNF', True, (255,255,255))
                        screen.blit(textsurface, (horsecharacter_rect.x + 160, horsecharacter_rect.y+8))
                    else:
                        textsurface = myfont.render(str(round((horse.endTime-horse.startTime)/1000,2)), True, (255,255,255))
                        screen.blit(textsurface, (horsecharacter_rect.x + 160, horsecharacter_rect.y+8))

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        #self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(config.screensize, pygame.FULLSCREEN|pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.horses = []
        names = ['Sea Biscuit','Sweeny','Secretariat','Sympatico']
        for horsenum, name in enumerate(names):
          self.horses.append(Horse(horsenum, name))

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
            #self.screen = pygame.transform.scale(self.screen, (config.tracksize[0]*2, config.tracksize[1]*2))
            surface = pygame.display.get_surface()
            data = pygame.image.tostring(surface,'RGB')
            img = Image.frombytes('RGB', config.tracksize, data)
            self.matrix.draw(img)
            pygame.display.update()


def start():
  settings = {
      'size': config.tracksize,
      'fps' :120
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

  app.matrix = MatrixScreen()

  app.title = pygame.image.load(os.path.join(config.imagePath, 'splash.png')).convert_alpha()
  app.results = pygame.image.load(os.path.join(config.imagePath, 'results.png')).convert_alpha()
  app.grass = pygame.image.load(os.path.join(config.imagePath, 'background_3.png'))

  app.setup_states(state_dict, 'start')
  app.main_game_loop()
  pygame.quit()


def parse_args(argv):
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=__doc__)

  parser.add_argument("-t", "--test", dest="test_flag", 
                    default=False,
                    action="store_true",
                    help="Run test function")
  parser.add_argument("--log-level", type=str,
                      choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                      help="Desired console log level")
  parser.add_argument("-d", "--debug", dest="log_level", action="store_const",
                      const="DEBUG",
                      help="Activate debugging")
  parser.add_argument("-q", "--quiet", dest="log_level", action="store_const",
                      const="CRITICAL",
                      help="Quite mode")
  #parser.add_argument("files", type=str, nargs='+')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, stdout, environ):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  logging.basicConfig(format="[%(asctime)s] %(levelname)-8s %(message)s", 
                    datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  start()

if __name__ == "__main__":
  main(sys.argv, sys.stdout, os.environ)
