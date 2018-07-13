from PIL import Image
import pygame



class AnimatedSprite():

    def __init__(self, imagename,frames):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        print("AnimatedSprite init: "+imagename)
        self.images = []
        for frameno in range(frames):
             image_frame_name=imagename+'_'+str(frameno)+'.png'
             print("AnimatedSprite loading: "+image_frame_name)
             self.images.append(Image.open(image_frame_name))
        self.index = 0
        self.image = self.images[self.index]  # 'image' is the current image of the animation.

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update(self, dt,screen,x,y):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        screen.paste(self.image,(x,y),self.image)

