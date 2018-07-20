#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image


class MatrixScreen():
    def __init__(self):
        # Configuration for the matrix
        self.options = RGBMatrixOptions()
        self.options.rows = 64
        self.options.cols = 64
        self.options.chain_length = 2
        self.options.parallel = 2
        self.options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

        self.matrix = RGBMatrix(options = self.options)
    def draw(self,image):
        self.matrix.SetImage(image.convert('RGB'))
