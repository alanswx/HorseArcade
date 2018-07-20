#!/usr/bin/env python
import time
import sys

from PIL import Image


class MatrixScreen():
    def __init__(self):
        self.x=1
    def draw(self,image):
        self.x=self.x+1
