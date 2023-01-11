#!/usr/bin/python
import numpy as np
from scipy import signal
import copy
'Edge Enhancement'
def main(ImageInfo, kernel):
    outputImageInfo = copy.deepcopy(ImageInfo)
    img = np.squeeze(ImageInfo.image[:,:,0]).astype(np.float32)
    outImg = np.clip(signal.convolve2d(img, kernel, mode = 'same', boundary= 'symm'), 0, 255)
    outputImageInfo.image[:,:,0] = outImg.astype(np.uint8)
    return outputImageInfo
    
