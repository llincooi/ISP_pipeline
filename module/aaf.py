#!/usr/bin/python
import numpy as np
import copy
from scipy import signal


def main(ImageInfo, mode):
    outputImageInfo = copy.deepcopy(ImageInfo)
    outputImageInfo.to_4ChDict()
    match mode:
        case 'mean':
            kernel = np.ones((3,3))/9.
        case 'median': pass
        case 'lowpass':
            kernel = np.array([[1, 2, 1],
                               [2, 4, 2],
                               [1, 2, 1]])/16
            
    for color in outputImageInfo.image.keys():
        outputImageInfo.image[color] = signal.convolve2d(outputImageInfo.image[color], kernel, mode = 'same').astype(np.uint16)
    return outputImageInfo
            

