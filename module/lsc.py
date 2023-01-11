import numpy as np
import copy
from scipy import interpolate
from scipy import signal

'Lens Shading Correlation'
def main(ImageInfo, LSCData, platform):
    outputImageInfo = copy.deepcopy(ImageInfo)
    outputImageInfo.to_4ChDict()
    if platform == 'Qualcomm':
        xStep = np.ceil(outputImageInfo.image['R'].shape[1]*np.arange(1/17/2, 1/2+1/17,1/17))
        xStep = (np.append(-xStep[::-1],xStep)+outputImageInfo.image['R'].shape[1]//2).astype(int)
        yStep = np.ceil(outputImageInfo.image['R'].shape[0]*np.arange(1/13/2, 1/2+1/13,1/13))
        yStep = (np.append(-yStep[::-1],yStep)+outputImageInfo.image['R'].shape[0]//2).astype(int)
        
        for color in outputImageInfo.image.keys():
            LSCArray = signal.convolve2d(LSCData[color].to_numpy().reshape(13,17), np.ones((3,3)), mode='same')/signal.convolve2d(np.ones((13,17)), np.ones((3,3)), mode='same')
            LSCArray = LSCArray/np.max(LSCArray)
            f = interpolate.interp2d((xStep[1:] + xStep[:-1])/2, (yStep[1:] + yStep[:-1])/2, LSCArray, kind = 'linear')
            LSCArray = f(range(outputImageInfo.image[color].shape[1]), range(outputImageInfo.image[color].shape[0]))
            outputImageInfo.image[color] = (outputImageInfo.image[color]/LSCArray).astype(np.uint16)
    return outputImageInfo