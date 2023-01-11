import numpy as np
import copy
from scipy import signal

'Noise Reduction for Luma'
def main(ImageInfo, windowSize, sigmaI, sigmaD, printProgress = False):
    outputImageInfo = copy.deepcopy(ImageInfo)
    
    img = np.squeeze(ImageInfo.image[:,:,0]).astype(np.float32)
    outImg = np.empty_like(img)
    
    img = signal.convolve2d(img, np.ones((3,3))/9., mode = 'same', boundary= 'symm') # a mean filter applied first
    for i in range(img.shape[0]):  # then apply bilateral filter 
        for j in range(img.shape[1]):
            upY = max(i-windowSize, 0)
            downY = min(i+windowSize+1, img.shape[0])
            leftX = max(j-windowSize, 0)
            rightY = min(j+windowSize+1, img.shape[1])
            weight = np.exp( -0.5*(((img[upY:downY,leftX:rightY] - img[i,j])/sigmaI)**2 +
                                   (((np.arange(upY,downY)-i)[:,np.newaxis]**2+(np.arange(leftX,rightY)-j)[np.newaxis,:]**2)/sigmaD**2)) )
            outImg[i,j] = np.sum(img[upY:downY,leftX:rightY]*weight/np.sum(weight))
        if i % 100 == 0 and printProgress:
            print(100*i//img.shape[0], "%")
    outputImageInfo.image[:,:,0] = outImg.astype(np.uint8)
    return outputImageInfo