# -*- coding: cp936 -*-
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
    if len(fns) == 0:
        raise Exception('open file error in reads(): ', path, extens)
    
    datas = np.zeros((len(fns), 3, h, w), int)
    for i, item in enumerate(fns):
        datas[i] = readPicData(path + '\\' + item, (w, h))

    return datas

def randArray(a, b, *args):
    np.random.seed(0)
    return np.random.rand(*args) * (b-a) + a


def im2col(inputData, filterH, filterW, stride=1, pad=0):
    N, C, H, W = inputData.shape
    # 计算输出数据的大小
    outH = (2*pad + H - filterH)//stride + 1
    outW = (2*pad + W - filterW)//stride + 1

    # 扩展
    img = np.pad(inputData, [(0,0), (0,0), (pad, pad), (pad, pad)], 'constant')

    col = np.zeros((N, C, filterH, filterW, outH, outW), dtype=int) # <= add dtype=int
    for y in range(filterH):
        yMax = y + stride*outH
        for x in range(filterW):
            xMax = x + stride*outW
            col[:, :, y, x, :, :] = img[:, :, y:yMax:stride, x:xMax:stride]

    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N*outH*outW, -1)
    return col

def col2im(col, inputShape, filterH, filterW, stride=1, pad=0):
    N, C, H, W = inputShape
    outH = (H + 2*pad - filterH)//stride + 1
    outW = (W + 2*pad - filterH)//stride + 1
    col = col.reshape(N, outH, outW, C, filterH, filterW).transpose(0, 3, 4, 5, 1, 2)

    img = np.zeros((N, C, H + 2*pad + stride - 1, W + 2*pad + stride - 1), dtype=int) # <= add dtype=int
    for y in range(filterH):
        yMax = y + stride*outH
        for x in range(filterW):
            xMax = x + stride*outW
            # bug here => img[:, :, y:yMax:stride, x:xMax:stride] += col[:, :, y, x, :, :]
            img[:, :, y:yMax:stride, x:xMax:stride] = col[:, :, y, x, :, :]
            
    return img[:, :, pad:H + pad, pad:W + pad]
