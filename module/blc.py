#!/usr/bin/python
import numpy as np
import copy

'Black Level Compensation'
def main(ImageInfo, parameters):
    outputImageInfo = copy.deepcopy(ImageInfo)
    outputImageInfo.to_4ChDict()
    raw4ChDict = outputImageInfo.image
    upLimit = 2**ImageInfo.bitNumber-1
    
    bl_r = parameters[0]
    bl_gr = parameters[1]
    bl_gb = parameters[2]
    bl_b = parameters[3]
    alpha = parameters[4]
    beta = parameters[5]
    
    # raw4ChDict['Gr'] = np.clip( raw4ChDict['Gr'] - bl_gr + alpha * raw4ChDict['R'], 0, upLimit)
    # raw4ChDict['Gb'] = np.clip( raw4ChDict['Gb'] - bl_gb + beta  * raw4ChDict['B'], 0, upLimit)
    raw4ChDict['Gr'] = np.clip( raw4ChDict['Gr'].astype(np.int32) - bl_gr, 0, upLimit).astype(np.uint16)
    raw4ChDict['Gb'] = np.clip( raw4ChDict['Gb'].astype(np.int32) - bl_gb, 0, upLimit).astype(np.uint16)
    raw4ChDict['R']  = np.clip( raw4ChDict['R'].astype(np.int32)  - bl_r, 0, upLimit).astype(np.uint16)
    raw4ChDict['B']  = np.clip( raw4ChDict['B'].astype(np.int32)  - bl_b, 0, upLimit).astype(np.uint16)

    outputImageInfo.image = raw4ChDict
    return outputImageInfo

