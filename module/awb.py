#!/usr/bin/python
import numpy as np
import copy

'Auto White Balance'
def main(ImageInfo, parameters):
    outputImageInfo = copy.deepcopy(ImageInfo)
    outputImageInfo.to_4ChDict()
    raw4ChDict = outputImageInfo.image
    upLimit = 2**ImageInfo.bitNumber-1
    
    r_gain = parameters[0]
    gr_gain = parameters[1]
    gb_gain = parameters[2]
    b_gain = parameters[3]

    raw4ChDict['Gr'] = np.clip( raw4ChDict['Gr'] *gr_gain, 0, upLimit).astype(np.uint16)
    raw4ChDict['Gb'] = np.clip( raw4ChDict['Gb'] *gb_gain, 0, upLimit).astype(np.uint16)
    raw4ChDict['R']  = np.clip( raw4ChDict['R'] *r_gain, 0, upLimit).astype(np.uint16)
    raw4ChDict['B']  = np.clip( raw4ChDict['B'] *b_gain, 0, upLimit).astype(np.uint16)
    
    outputImageInfo.image = raw4ChDict
    return outputImageInfo
