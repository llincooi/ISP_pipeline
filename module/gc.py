#!/usr/bin/python
import numpy as np
import copy

'Gamma Correction'
def main(ImageInfo, gamma):
    outputImageInfo = copy.deepcopy(ImageInfo)
    outputImageInfo.image = ImageInfo.image**gamma
    return outputImageInfo