#! /usr/bin/env python3

import os, sys, string, time, logging, argparse

import pygame
from PIL import Image
import AnimatedSprite
import BlinkingLED
try:
    import dispense
except:
  import dispensenull as dispense

try:
  import RPi.GPIO as GPIO
except:
  import nullgpio as GPIO



try:
  import config
except ImportError:
  print ("no config.py found.  Please copy sample_config.py to config.py.")
  sys.exit(1)

#
# Setup GPIO pins for LEDs
#
GPIO.setmode(GPIO.BCM)
for io in config.horseLeds:
  GPIO.setup(io,GPIO.OUT)



x = 0
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)


SONG_END = pygame.USEREVENT + 1

class Horse:
    def __init__(self, slotnumber, name,leds):
        self.name = name
        self.slotnumber = slotnumber
        self.leds = leds
        dispense.dispense_init()
        horsePath = os.path.join(config.imagePath, 'horse_%d' % (slotnumber+1))
        self.sprite = AnimatedSprite.AnimatedSprite(os.path.join(horsePath, 'frame'), 12)
        self.blinkingLEDs = BlinkingLED.BlinkingLED(GPIO,self.leds[0],self.leds[1],animation_time=0.2)
        self.still = pygame.image.load(os.path.join(horsePath, 'still.png'))
        self.character = pygame.image.load(os.path.join(horsePath, 'face.png')).convert_alpha()
        self.reset()

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

        self.startTime = None
        self.endTime = None
        self.setLEDs()

    def reset_time(self):
        self.startTime = time.time()
        self.endTime = time.time()

    def draw(self, screen, dt):
      if self.hidden:
          return

      if self.done or self.startTime is None:
        screen.blit(self.still, [self.x,self.y])
      else:
        self.sprite.update(dt,screen,self.x,self.y)
        if not self.done:
          if self.x <= config.finishlinex:
            self.done = True
            self.endTime = time.time()

    def updateLEDs(self,dt):
        if self.hidden:
            self.blinkingLEDs.update(dt)

    def setLEDs(self):
        #print('setLEDs')
        if self.x < config.finishlinex:
             GPIO.output(self.leds[0],0)
             GPIO.output(self.leds[1],0)
             #print('setLEDs: self.x < config.finishlinex',self.x,config.finishlinex)
        else:
          if (self.feet==0):
             GPIO.output(self.leds[0],0)
             GPIO.output(self.leds[1],1)
          else:
             GPIO.output(self.leds[1],0)
             GPIO.output(self.leds[0],1)

    def change_state(self):
        GPIO.output(self.leds[0],0)
        GPIO.output(self.leds[1],0)

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
        self.setLEDs()

class Grass:
  def __init__(self):
    self.grass = pygame.image.load(os.path.join(config.imagePath, 'background_3.png'))

  def draw(self, screen, pos):
    screen.blit(self.grass, pos)

class Grass2:
  def __init__(self):
    self.wheel = pygame.image.load(os.path.join(config.imagePath, 'track', 'wheel.png'))
    self.uppertrack = pygame.image.load(os.path.join(config.imagePath, 'track', 'uppertrack.png'))
    self.lowertrack = pygame.image.load(os.path.join(config.imagePath, 'track', 'lowertrack.png'))

  def draw(self, screen, pos):
    x = pos[0]
    y = pos[1]

    greens = []
    hgreens = []
    greens.append((142, 252, 3)) ## first
    hgreens.append((26, 223, 1))

    greens.append((33, 223, 1))
    hgreens.append((48, 227, 2))

    greens.append((114, 244, 14))
    hgreens.append((59, 227, 34))

    greens.append((33, 223, 1))  ## extra
    hgreens.append((48, 227, 2))

    greens.append((142, 252, 3)) ## extra 2
    hgreens.append((26, 223, 1))

    greens.append((13, 202, 4))
    hgreens.append((25, 209, 21))

    greens.append((38, 221, 42))  ## last
    hgreens.append((7, 195, 6))

    #screen.set_clip((0,0,config.tracksize[0], config.tracksize[1]))


    screen.blit(self.uppertrack, [x, y])
    if self.uppertrack.get_size()[0]+x < config.tracksize[0]:
      screen.blit(self.uppertrack, [self.uppertrack.get_size()[0]+x, y])

    screen.blit(self.wheel, [x+15, y+11])

    y += self.uppertrack.get_size()[1]
    pygame.draw.rect(screen, greens[0], (x, y, config.tracksize[0], config.horsesize[1]))

    y += int(config.horsesize[1]/2)
    dy = config.horsesize[1]-1
    for n in range(len(config.horseNames)-1):
      pygame.draw.rect(screen, greens[n+1], (x, y, config.tracksize[0], dy))
      pygame.draw.rect(screen, hgreens[n+1], (x, y+dy, config.tracksize[0], dy+1))
      y += config.horsesize[1]

    y -= 2
    screen.blit(self.lowertrack, [pos[0], y])
    if self.lowertrack.get_size()[0]+x < config.tracksize[0]:
      screen.blit(self.lowertrack, [self.lowertrack.get_size()[0]+pos[0], y])
    screen.blit(self.wheel, [x+15, y - 8])


class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Splash(States):
    def __init__(self, app):
        self.app = app
        States.__init__(self)
        self.next = 'start'

    def startup(self):
        logging.debug('starting Splash state')
        self.timerStarted = True
        self.time = 3
    def get_event(self, event):
        if event.type == pygame.JOYBUTTONUP:
          logging.debug("Joystick button released.")
          logging.debug(event)
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE: self.quit = True


    def update(self, screen, dt):
        self.draw(screen, dt)
        if self.timerStarted == True:
            self.time = self.time - dt
        if self.time < 0 and self.timerStarted == True:
            self.done = True

    def draw(self, screen, dt):
            screen.blit(self.app.title, [0,0])

class Start(States):
    def __init__(self, app):
        self.app = app
        States.__init__(self)
        self.next = 'countdown'

    def startup(self):
        self.timerStarted = False
        self.time = 3
        self.app.resetHorses()
        logging.debug('starting Start state')

    def get_event(self, event):
        if event.type == pygame.JOYBUTTONUP:
            logging.debug("Joystick button released.")
            logging.debug(event)
            if event.button==0: self.app.addHorse(0)
            elif event.button==1: self.app.addHorse(0)
            elif event.button==2: self.app.addHorse(1)
            elif event.button==3: self.app.addHorse(1)
            elif event.button==4: self.app.addHorse(2)
            elif event.button==5: self.app.addHorse(2)
            elif event.button==6: self.app.addHorse(3)
            elif event.button==7: self.app.addHorse(3)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: self.quit = True
            elif event.key == pygame.K_3: self.app.addHorse(0)
            elif event.key == pygame.K_e: self.app.addHorse(1)
            elif event.key == pygame.K_d: self.app.addHorse(2)
            elif event.key == pygame.K_c: self.app.addHorse(3)
            elif event.key == pygame.K_y: self.app.addHorse(4)
            elif event.key == pygame.K_h: self.app.addHorse(5)

        if self.app.numPeople() >= config.minpeople:
          self.timerStarted = True
        if self.app.numPeople() == len(config.horseNames):
            self.done = True

    def update(self, screen, dt):
        self.draw(screen, dt)
        if self.timerStarted == True:
            self.time = self.time - dt
        if self.time < 0 and self.timerStarted == True:
            self.done = True
        for horse in self.app._horses:
            horse.updateLEDs(dt)

    def draw(self, screen, dt):
        screen.blit(self.app.results2, [0,0])
        for horse in self.app._horses:
          readytext = self.app.ribbon[0]
          ready_rect = readytext.get_rect()
          ready_rect.x = ((horse.slotnumber) * 128)+64-ready_rect.width/2
          ready_rect.y = 58
          myfont = pygame.font.SysFont(os.path.join(config.fontPath, 'Bebas Neue.ttf'), 25)
          if horse.hidden:
              textsurface = myfont.render('Press Any', True, (0,0,0))
              screen.blit(textsurface, (ready_rect.x-32, ready_rect.y+16))
              textsurface = myfont.render('Button', True, (0,0,0))
              screen.blit(textsurface, (ready_rect.x-16, ready_rect.y+32))
              if self.timerStarted == True:
                  textsurface = myfont.render(str(round(self.time)), True, (0,0,0))
                  screen.blit(textsurface, (ready_rect.x+12, ready_rect.y+48))
          else:
              textsurface = myfont.render('Ready!', True, (0,0,0))
              screen.blit(textsurface, (ready_rect.x-8, ready_rect.y+16))
class CountDown(States):
    def __init__(self, app):
        self.sprite=AnimatedSprite.AnimatedSprite(os.path.join(config.imagePath, 'countdown'), 6, 5,offset=-1,animation_time=1)
        self.app = app
        States.__init__(self)
        self.next = 'game'

    def startup(self):
        self.timerStarted = True
        self.time = 6
        logging.debug('starting Countdown state')
        pygame.mixer.music.load(os.path.join(config.soundPath, 'racestart.ogg'))
        pygame.mixer.music.set_endevent(SONG_END)
        pygame.mixer.music.play(0)
        for horse in self.app.horses():
            horse.setLEDs()
    def get_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: self.quit = True

    def update(self, screen, dt):
        self.draw(screen, dt)
        if self.timerStarted == True:
            self.time = self.time - dt
        if self.time < 0 and self.timerStarted == True:
            self.done = True

    def draw(self, screen, dt):
        self.app.grass.draw(screen, [0,0])
        if self.timerStarted == True:
            self.sprite.update(dt, screen,
                           x=(config.tracksize[0] - self.sprite.image.get_rect()[2])/2,
                           y=(config.tracksize[1] - self.sprite.image.get_rect()[3])/2)
        for horse in self.app.horses():
          horse.draw(screen, dt)

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
        for horse in self.app.horses():
            horse.reset_time()
            horse.setLEDs()
        logging.debug('starting Game state')

    def get_event(self, event):
          if event.type == SONG_END:
            logging.debug("the song ended!")
            pygame.mixer.music.load(os.path.join(config.soundPath, 'horsesounds.ogg'))
            pygame.mixer.music.play(0)

          if event.type == pygame.JOYBUTTONUP:
            logging.debug("Joystick button released.")
            logging.debug(event)
            if   event.button==0: self.app.getHorse(0).button(0)
            elif event.button==1: self.app.getHorse(0).button(1)
            elif event.button==2: self.app.getHorse(1).button(0)
            elif event.button==3: self.app.getHorse(1).button(1)
            elif event.button==4: self.app.getHorse(2).button(0)
            elif event.button==5: self.app.getHorse(2).button(1)
            elif event.button==6: self.app.getHorse(3).button(0)
            elif event.button==7: self.app.getHorse(3).button(1)
          elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_1: self.app.getHorse(0).button(0)
            elif event.key == pygame.K_2: self.app.getHorse(0).button(1)
            elif event.key == pygame.K_q: self.app.getHorse(1).button(0)
            elif event.key == pygame.K_w: self.app.getHorse(1).button(1)
            elif event.key == pygame.K_a: self.app.getHorse(2).button(0)
            elif event.key == pygame.K_s: self.app.getHorse(2).button(1)
            elif event.key == pygame.K_z: self.app.getHorse(3).button(0)
            elif event.key == pygame.K_x: self.app.getHorse(3).button(1)
            elif event.key == pygame.K_ESCAPE:
              self.quit = True

    def update(self, screen, dt):
        self.draw(screen, dt)
        if self.timerStarted == True:
            self.time = self.time - dt
        horses = self.app.horses()

        if not self.timerStarted:
          for horse in horses:
            if horse.done:
              self.timerStarted = True

        ## check if all of the horse are done
        if self.timerStarted:
          dones = [horse.done for horse in horses if not horse.done]
          if len(dones) == 0:
            self.done = True

          ## check if the finish timer has run out
          if self.time < 0: self.done = True

    def draw(self, screen, dt):
        self.app.grass.draw(screen, [0,0])

        horses = self.app.horses()
        for horse in horses: horse.draw(screen, dt)

        if self.timerStarted == True:
          self.sprite.update(dt, screen,
                             x=(config.tracksize[0] - self.sprite.image.get_rect()[2])/2,
                             y=(config.tracksize[1] - self.sprite.image.get_rect()[3])/2)

class Finish(States):
    def __init__(self, app):
        self.app = app
        States.__init__(self)
        self.next = 'splash'

        self.showTimer = None

    def startup(self):
        logging.debug('starting Finish state')
        pygame.mixer.music.load(os.path.join(config.soundPath, 'finish.ogg'))
        pygame.mixer.music.play(0)
        self.sortedList = sorted(self.app.horses(), key=lambda horse: (not horse.done, horse.endTime-horse.startTime, horse.x))
        for horse in self.app.horses():
          dt = horse.endTime - horse.startTime
          logging.info("%d: %.3f" % ((horse.slotnumber+1), dt))
        self.dispensed_candy = False
##           if dt == 0:
##             horse.endTime = None

    def get_event(self, event):
        if event.type == pygame.JOYBUTTONUP:
          logging.debug("Joystick button released.")
          logging.debug(event)
          if event.button in (0,2,4,6):
            self.markDone()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.markDone()
        elif event.type == pygame.KEYDOWN:
          if event.key in (pygame.K_1, pygame.K_q, pygame.K_a, pygame.K_z):
            self.markDone()
          elif event.key == pygame.K_ESCAPE: self.quit = True

    def markDone(self):
      dt = time.time() - self.showTimer
      if dt > 5:
        self.done = True

    def update(self, screen, dt):
        self.draw(screen)
        pygame.display.flip()

    def draw(self, screen):
        screen.blit(self.app.results2, [0,0])

        for place, horse in enumerate(self.sortedList):

          #logging.debug((col,row))
          #logging.debug(str(horse.slotnumber+1)+': '+str((horse.endTime-horse.startTime))+' '+str(horse.x))
          #print(str(horse.slotnumber+1)+': '+str((horse.endTime-horse.startTime))+' '+str(horse.x))
          #print(horse.name,place)
          ribbon = self.app.ribbon[place]
          ribbon_rect = ribbon.get_rect()
          ribbon_rect.x = ((horse.slotnumber) * 128)+64-ribbon_rect.width/2
          ribbon_rect.y = 58
          #print(ribbon_rect)

          screen.blit(ribbon, ribbon_rect)

          myfont = pygame.font.SysFont(os.path.join(config.fontPath, 'Bebas Neue.ttf'), 20)
          if not horse.done:
              textsurface = myfont.render('DNF', True, (0,0,0))
              screen.blit(textsurface, (ribbon_rect.x, ribbon_rect.y+56))
          else:
              textsurface = myfont.render(str(round((horse.endTime-horse.startTime),2)), True, (0,0,0))
              screen.blit(textsurface, (ribbon_rect.x, ribbon_rect.y+56))
          if not self.dispensed_candy:
              winner = self.sortedList[0].slotnumber
              #print("The winner is " + str(winner+1))
              for horse in self.app.horses():
                dispense.dispense_back(horse.slotnumber)
              time.sleep(1)
              for horse in self.app.horses():
                dispense.dispense_forward(horse.slotnumber)
              dispense.dispense_back(winner)
              dispense.dispense_forward(winner)
              self.showTimer = time.time()
              self.dispensed_candy = True

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        #self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode(config.screensize, pygame.FULLSCREEN|pygame.DOUBLEBUF)
        self.screen = pygame.display.set_mode()
        try:
            GPIO.setsurface(self.screen)
            # Method exists, and was used.
        except AttributeError:
            # Method does not exist.  What now?
            print('traditional GPIO')

        self.clock = pygame.time.Clock()
        self._horses = []
        for horsenum, name in enumerate(config.horseNames):
          self._horses.append(Horse(horsenum, name,config.horseLeds[horsenum]))

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()

    def flip_state(self):
        for horse in self._horses:
            horse.change_state()
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def horses(self):
      horses = [horse for horse in self._horses if not horse.hidden]
      return horses

    def getHorse(self, horseid):
      return self._horses[horseid]

    def numPeople(self):
      return len(self.horses())

    def addHorse(self, horseid):
      if self._horses[horseid].hidden:
        logging.debug('Player %d joined' % horseid)
        logging.debug('There are %d people ready' % self.numPeople())
      self._horses[horseid].show()

    def resetHorses(self):
      for horse in self._horses:
        horse.reset()

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
            #surface = pygame.display.get_surface()
            #data = pygame.image.tostring(surface,'RGB')
            #img = Image.frombytes('RGB', config.tracksize, data)
            #self.matrix.draw(img)
            pygame.display.update()
            pygame.display.flip()


def start():
  settings = {
      'size': config.tracksize,
      'fps' :120
  }

  app = Control(**settings)
  state_dict = {
      'splash': Splash(app),
      'start': Start(app),
      'countdown': CountDown(app),
      'game': Game(app),
      'finish':Finish(app)
  }

  pygame.init()
  pygame.joystick.init()
  joystick_count = pygame.joystick.get_count()
  for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

  #app.matrix = MatrixScreen()
  pygame.mouse.set_visible(False)
  app.title = pygame.image.load(os.path.join(config.imagePath, 'splash.png')).convert_alpha()
  app.results2 = pygame.image.load(os.path.join(config.imagePath, 'results2.png')).convert_alpha()
  app.results = pygame.image.load(os.path.join(config.imagePath, 'results.png')).convert_alpha()
  app.ribbon = [
   pygame.image.load(os.path.join(config.imagePath, 'ribbons/ribbon1.png')).convert_alpha(),
   pygame.image.load(os.path.join(config.imagePath, 'ribbons/ribbon2.png')).convert_alpha(),
   pygame.image.load(os.path.join(config.imagePath, 'ribbons/ribbon3.png')).convert_alpha(),
   pygame.image.load(os.path.join(config.imagePath,'ribbons/ribbon4.png')).convert_alpha()]

  app.grass = Grass2()

  app.setup_states(state_dict, 'splash')
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
