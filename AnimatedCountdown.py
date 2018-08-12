from PIL import Image
import pygame



class AnimatedSprite():

    def __init__(self, imagename,frames, index):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        print("AnimatedSprite init: "+imagename)
        self.images = []
        for frameno in range(frames):
             image_frame_name=imagename+format(frameno)+'.png'
             print("AnimatedSprite loading: "+image_frame_name)
             self.images.append(pygame.image.load(image_frame_name).convert_alpha())
        self.index = index
        self.image = self.images[self.index]  # 'image' is the current image of the animation.
        self.animation_time = 1
        self.current_time = 0

        self.current_frame = 0
        self.end = pygame.image.load('images/endgame.png').convert_alpha()
        self.end_rect = self.end.get_rect()
    def update(self, dt, screen):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index - 1) % len(self.images)
            self.image = self.images[self.index]
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (256, 64)
        screen.blit(self.image, self.image_rect)
        self.image_rect.center = (256, 64)
        pygame.display.update
    def update1(self, dt, screen):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index - 1) % len(self.images)
            self.image = self.images[self.index]
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (384, 64)
        screen.blit(self.image, self.image_rect)
        self.end_rect.center = (192,64)
        screen.blit(self.end, self.end_rect)
        pygame.display.update
