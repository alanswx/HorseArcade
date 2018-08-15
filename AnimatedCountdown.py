from PIL import Image
import pygame



class AnimatedSprite():

    def __init__(self, imagename, frames, index = 0, label=None,offset=1,animation_time=.1):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        print("AnimatedSprite init: "+imagename)
        self.images = []
        for frameno in range(frames):
             image_frame_name=imagename+str('{0:02d}'.format(frameno+1))+'.png'
             print("AnimatedSprite loading: "+image_frame_name)
             self.images.append(pygame.image.load(image_frame_name).convert_alpha())
        self.index = index
        self.image = self.images[self.index]  # 'image' is the current image of the animation.
        self.animation_time = animation_time
        self.current_time = 0
        self.offset=offset

        self.current_frame = 0
        self.label = label
        #self.label = pygame.image.load('images/endgame.png').convert_alpha()
        if self.label:
            self.label_rect = self.label.get_rect()
    def update(self, dt, screen, x=None,y=None):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        width = screen.get_width()
        height = screen.get_height()

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + self.offset) % len(self.images)
            self.image = self.images[self.index]
        self.image_rect = self.image.get_rect()
        if not x:
            self.image_rect.center = (width/2, height/2)
            screen.blit(self.image, self.image_rect)

        else:
            screen.blit(self.image, [x,y])
        if self.label:
            self.image_rect.center = (width - (width/8), height/2) #should be calculated later
            screen.blit(self.image, self.image_rect)
            self.label_rect.center = (width/2,height/2)
            screen.blit(self.label, self.label_rect)
        pygame.display.update()
