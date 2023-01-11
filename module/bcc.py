#!/usr/bin/python
import numpy as np
import copy

'Brightness Contrast Control'
def main(ImageInfo, brightness, contrast):
    outputImageInfo = copy.deepcopy(ImageInfo)
    img = np.squeeze(ImageInfo.image[:,:,0]).astype(np.float32)
    outImg = np.clip( contrast*(img-128)+128 + brightness, 0, 255)
    outputImageInfo.image[:,:,0] = outImg.astype(np.uint8)
    return outputImageInfo
