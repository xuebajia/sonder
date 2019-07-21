import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image

def readPicData(fn, imSize):
    print '[+] Reading picture data from {}'.format(fn)
    try:
        img = Image.open(fn)
        img = img.convert('RGB')
        img = img.resize(imSize)
        data = np.array(img)
    except IOError:
        raise Exception('open file error in readPicData(): ', fn)

    return data
