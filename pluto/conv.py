import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image

from func import *

class conv:
    def __init(self, w, h):
        self.pad = 0
        self.stride = 1
        
        self.imSize = (w, h)
        self.fiSize = (16, 16)
        
        self.img = None
        self.filter = None

    def read(fn):
        self.img = readPicData('img.png', self.imSize)
