# -*- coding: cp936 -*-
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
#from globalData import *

from func import *

class conv:
    def __init__(self, W, stride=1, pad=0):
        self.stride = stride    # 步幅
        self.pad = pad          # 填充
        self.W = W              # 卷积核 4维
        self.x = None           # 数据
        self.col = None
        self.colW = None
        self.dW = None          # 权重


    def forward(self, x):
        FN, C, FH, FW = self.W.shape # 卷积核的大小
        N, C, H, W = x.shape         # 数据的大小

        # 计算输出数据的大小
        outW = 1 + int((W + 2*self.pad - FW)/self.stride)
        outH = 1 + int((H + 2*self.pad - FH)/self.stride)

        # 用im2col 将数据转换为行
        col = im2col(x, FH, FW, self.stride, self.pad)
        # 将卷积核转换为列, 然后展开为二维数组
        colW = self.W.reshape(FN, -1).T

        # 正向传播
        out = np.dot(col, colW)
        out = out.reshape(N, outH, outW, -1).transpose(0, 3, 1, 2)

        self.x = x
        self.col = col
        self.colW = colW

        return out

    def backward(self, dout):
        FN, C, FH, FW = self.W.shape # 卷积核的大小
        dout = dout.transpose(0, 2, 3, 1).reshape(-1, FN)

        self.dW = np.dot(self.col.T, dout)
        self.dW = self.dW.transpose(1, 0).reshape(FN, C, FH, FW)

        dcol = np.dot(dout, self.colW.T)
        dx = col2im(dcol, self.x.shape, FH, FW, self.stride, self.pad)

        return dx


def test():
    np.random.seed(0)
    w = np.random.randint(0, 2, (1, 3, 3, 3))
    #x = np.random.randint(0, 3, (1, 1, 5, 5))
    x = reads(path.abspath('sample'), 'png', 5, 5)
    print 'w => \n', w
    print 'x => \n', x
    c = conv(w, 1, 0)
    out = c.forward(x)
    print 'out => \n', out
    dx = c.backward(out)
    print 'dx => \n', dx


if __name__ == '__main__':
    test()
