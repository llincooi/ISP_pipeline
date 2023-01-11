#!/usr/bin/python
import numpy as np
import copy

'Hue Saturation Control'
def main(ImageInfo, hueTheta, saturation):
    outputImageInfo = copy.deepcopy(ImageInfo)
    UVimg = ImageInfo.image[:,:,1:,np.newaxis].astype(np.float32) - 128
    hue = np.array([[ np.cos(hueTheta), np.sin(hueTheta)],
                    [-np.sin(hueTheta), np.cos(hueTheta)]])
    outImg = saturation*np.matmul(hue, UVimg) + 128
    outputImageInfo.image[:,:,1:] = np.clip(np.squeeze(outImg), 0, 255).astype(np.uint8)
    return outputImageInfo
