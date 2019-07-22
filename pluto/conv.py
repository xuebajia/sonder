import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
from globalData import *

from func import *

class conv:
    def __init(self):
        self.imgs = None
        self.filter = None

    def convolution(self, fp, extens):
        self.imgs = reads(fp, extens, imageW, imageH)
        print self.imgs.shape
        a = im2col(self.imgs, filterH, filterW, 1, 0)
        print a.shape

a = conv()
a.convolution(path.abspath('sample'), 'png')

