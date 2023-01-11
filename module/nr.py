import numpy as np
import copy
from scipy import signal

'Noise Reduction'
def main(ImageInfo, windowSize, sigmaI, sigmaD, printProgress = False):
    outputImageInfo = copy.deepcopy(ImageInfo)
    
    img = ImageInfo.image.astype(np.float32)
    outImg = np.empty_like(img)
    
    img[:,:,0] = signal.convolve2d(img[:,:,0], np.ones((3,3))/9., mode = 'same', boundary= 'symm') # a mean filter applied on All channel first
    outImg[:,:,1] = signal.convolve2d(img[:,:,1], np.ones((5,5))/25., mode = 'same', boundary= 'symm')
    outImg[:,:,2] = signal.convolve2d(img[:,:,2], np.ones((5,5))/25., mode = 'same', boundary= 'symm')
    for i in range(img.shape[0]):  # then apply bilateral filter on Y channel only
        for j in range(img.shape[1]):
            upY = max(i-windowSize, 0)
            downY = min(i+windowSize+1, img.shape[0])
            leftX = max(j-windowSize, 0)
            rightY = min(j+windowSize+1, img.shape[1])
            weight = np.exp( -0.5*(((img[upY:downY,leftX:rightY,0] - img[i,j,0])/sigmaI)**2 +
                                   (((np.arange(upY,downY)-i)[:,np.newaxis]**2+(np.arange(leftX,rightY)-j)[np.newaxis,:]**2)/sigmaD**2)) )
            outImg[i,j,0] = np.sum(img[upY:downY,leftX:rightY,0]*weight/np.sum(weight), axis = (0,1))
        if i % 100 == 0 and printProgress:
            print(100*i//img.shape[0], "%")
    outputImageInfo.image = outImg.astype(np.uint8)
    return outputImageInfo