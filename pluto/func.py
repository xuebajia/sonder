import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from PIL import Image
from os import listdir, path

#sample = path.abspath('sample')

def readPicData(fn, imSize):
    print '[+] Reading picture data from {}'.format(fn)
    try:
        # data.shape = (c, h, w)
        img = Image.open(fn)
        img = img.convert('RGB')
        img = img.resize(imSize)
        data = np.array(img)
        data = data.transpose(2, 0, 1)
    except IOError:
        raise Exception('open file error in readPicData(): ', fn)
    
    return data

def reads(path, extens, w, h):
    # datas.shape = (n, c, h, w)
    fns = listdir(path)
    fns = [item for item in fns if item.split('.')[-1] == extens]
    datas = np.zeros((len(fns), 3, h, w), int)
    for i, item in enumerate(fns):
        datas[i] = readPicData(path + '\\' + item, (w, h))

    return datas

def randArray(a, b, *args):
    np.random.seed(0)
    return np.random.rand(*args) * (b-a) + a


def im2col(datas, hF, wF, stride=1, pad=0):
    # data (n, c, h, w)

    N, C, H, W = datas.shape
    outH = (2*pad + H - hF)/stride + 1
    outW = (2*pad + W - wF)/stride + 1

    img = np.pad(datas, [(0, 0), (0, 0), (pad, pad), (pad, pad)], 'constant')
    col = np.zeros((N, C, hF, wF, outH, outW))

    for y in range(hF):
        yMax = y + stride*outH
        for x in range(wF):
            xMax = x + stride*outW
            col[:, :, y, x, :, :] = img[:, :, y:yMax:stride, x:xMax:stride]

    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N*outH*outW, -1)
    return col

'''
x = np.random.rand(3, 3, 4, 4)
print(im2col(x,2,2,2,0))
print(im2col(x,2,2,2,0).shape)
'''
