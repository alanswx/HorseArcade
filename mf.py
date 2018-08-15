#!/usr/bin/env python
import time
import sys

from PIL import Image

from flaschen import Flaschen

class MatrixScreen():
    def __init__(self):
        # Configuration for the matrix
        self.sizex=512
        self.sizey=128
        self.fl = Flaschen('10.0.2.55',1337,self.sizex,self.sizey)
        self.lastimage=None
    def draw(self,image):
        lastimage = self.lastimage
        self.lastimage =image.tobytes()
        if lastimage!=self.lastimage:
           ni = image.resize((self.sizex,self.sizey), Image.ANTIALIAS)
           self.fl.setdata(ni.tobytes())
           self.fl.send()
