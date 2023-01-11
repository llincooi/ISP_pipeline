#!/usr/bin/python
import numpy as np
import copy

'Color Correction Matrix'
def main(ImageInfo, ccm):
    outputImageInfo = copy.deepcopy(ImageInfo)
    if ccm.shape[1] == 3:
        outputImageInfo.image = np.clip(np.squeeze(np.matmul(ccm[np.newaxis, np.newaxis, :, :], ImageInfo.image[:,:,:,np.newaxis])), 0, 1).astype(np.float16)
    else:
        outputImageInfo.image = np.clip(np.squeeze(np.matmul(ccm[np.newaxis, np.newaxis, :, :3], ImageInfo.image[:,:,:,np.newaxis])) + ccm[:, 3], 0, 1).astype(np.float16)
    return outputImageInfo
