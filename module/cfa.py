import numpy as np
import copy

'Color Filter Array Interpolation'

def G_at_RB(imgPad, pos):
    x = int(pos[1] + 3)
    y = int(pos[0] + 3)
    return (2*(imgPad[y-1:-7+(y-1):2, x:-7+x:2]+imgPad[y+1:-7+(y+1):2, x:-7+x:2]+imgPad[y:-7+y:2, x-1:-7+(x-1):2]+imgPad[y:-7+y:2, x+1:-7+(x+1):2])+
            4*imgPad[y:-7+y:2, x:-7+x:2]-imgPad[y-2:-7+(y-2):2, x:-7+x:2]-imgPad[y+2:-7+(y+2):2, x:-7+x:2]-imgPad[y:-7+y:2, x-2:-7+(x-2):2]-imgPad[y:-7+y:2, x+2:-7+(x+2):2])/8

def RB_at_BR(imgPad, pos):
    x = int(pos[1] + 3)
    y = int(pos[0] + 3)
    return (6*imgPad[y:-7+y:2, x:-7+x:2] +
            2*(imgPad[y-1:-7+(y-1):2, x-1:-7+(x-1):2]+imgPad[y-1:-7+(y-1):2, x+1:-7+(x+1):2]+imgPad[y+1:-7+(y+1):2, x-1:-7+(x-1):2]+imgPad[y+1:-7+(y+1):2, x+1:-7+(x+1):2])
            -0.5*(imgPad[y:-7+(y):2, x-2:-7+(x-2):2]+imgPad[y:-7+(y):2, x+2:-7+(x+2):2]+imgPad[y-2:-7+(y-2):2, x:-7+(x):2]+imgPad[y+2:-7+(y+2):2, x:-7+(x):2]))/8

def RB_at_row(imgPad, pos):
    x = int(pos[1] + 3)
    y = int(pos[0] + 3)
    return (5*imgPad[y:-7+y:2, x:-7+x:2] + 4*(imgPad[y:-7+(y):2, x-1:-7+(x-1):2]+imgPad[y:-7+(y):2, x+1:-7+(x+1):2])
            -(imgPad[y-1:-7+(y-1):2, x-1:-7+(x-1):2]+imgPad[y-1:-7+(y-1):2, x+1:-7+(x+1):2]+imgPad[y+1:-7+(y+1):2, x-1:-7+(x-1):2]+imgPad[y+1:-7+(y+1):2, x+1:-7+(x+1):2]+
              imgPad[y-2:-7+(y-2):2, x:-7+(x):2]+imgPad[y+2:-7+(y+2):2, x:-7+(x):2]) +
            0.5*(imgPad[y:-7+(y):2, x-2:-7+(x-2):2]+imgPad[y:-7+(y):2, x+2:-7+(x+2):2]))/8


def RB_at_column(imgPad, pos):
    x = int(pos[1] + 3)
    y = int(pos[0] + 3)
    return (5*imgPad[y:-7+y:2, x:-7+x:2] + 4*(imgPad[y-1:-7+(y-1):2, x:-7+(x):2]+imgPad[y+1:-7+(y+1):2, x:-7+(x):2])
            -(imgPad[y-1:-7+(y-1):2, x-1:-7+(x-1):2]+imgPad[y-1:-7+(y-1):2, x+1:-7+(x+1):2]+imgPad[y+1:-7+(y+1):2, x-1:-7+(x-1):2]+imgPad[y+1:-7+(y+1):2, x+1:-7+(x+1):2]+
              imgPad[y:-7+(y):2, x-2:-7+(x-2):2]+imgPad[y:-7+(y):2, x+2:-7+(x+2):2]) +
            0.5*(imgPad[y-2:-7+(y-2):2, x:-7+(x):2]+imgPad[y+2:-7+(y+2):2, x:-7+(x):2]))/8
    

def main(ImageInfo):
    ImageInfo.to_raw()
    imgPad = np.pad(ImageInfo.image, (3,3), 'reflect').astype(np.float16) # pad one more dummy side for indexing
    cfa_img = np.empty(list(ImageInfo.image.shape)+[3])
    match ImageInfo.bayerPattern:
        case 'RGGB':
            # G
            cfa_img[::2, ::2 ,1] = G_at_RB(imgPad, (0,0))
            cfa_img[::2, 1::2,1] = ImageInfo.image[::2, 1::2]
            cfa_img[1::2,::2 ,1] = ImageInfo.image[1::2,::2]
            cfa_img[1::2,1::2,1] = G_at_RB(imgPad, (1,1))
            # R
            cfa_img[::2, ::2 ,0] = ImageInfo.image[::2, ::2]
            cfa_img[::2, 1::2,0] = RB_at_row(imgPad, (0,1))
            cfa_img[1::2,::2 ,0] = RB_at_column(imgPad, (1,0))
            cfa_img[1::2,1::2,0] = RB_at_BR(imgPad, (1,1))
            # B
            cfa_img[::2, ::2 ,2] = RB_at_BR(imgPad, (0,0))
            cfa_img[::2, 1::2,2] = RB_at_column(imgPad, (0,1))
            cfa_img[1::2,::2 ,2] = RB_at_row(imgPad, (1,0))
            cfa_img[1::2,1::2,2] = ImageInfo.image[1::2,1::2]
            
        case 'BGGR':
            # G
            cfa_img[::2, ::2 ,1] = G_at_RB(imgPad, (0,0))
            cfa_img[::2, 1::2,1] = ImageInfo.image[::2, 1::2]
            cfa_img[1::2,::2 ,1] = ImageInfo.image[1::2,::2]
            cfa_img[1::2,1::2,1] = G_at_RB(imgPad, (1,1))
            # R
            cfa_img[::2, ::2 ,0] = RB_at_BR(imgPad, (0,0))
            cfa_img[::2, 1::2,0] = RB_at_column(imgPad, (0,1))
            cfa_img[1::2,::2 ,0] = RB_at_row(imgPad, (1,0))
            cfa_img[1::2,1::2,0] = ImageInfo.image[1::2,1::2]
            # B
            cfa_img[::2, ::2 ,2] = ImageInfo.image[::2, ::2]
            cfa_img[::2, 1::2,2] = RB_at_row(imgPad, (0,1))
            cfa_img[1::2,::2 ,2] = RB_at_column(imgPad, (1,0))
            cfa_img[1::2,1::2,2] = RB_at_BR(imgPad, (1,1))

        case 'GBRG':
            # G
            cfa_img[::2, ::2 ,1] = ImageInfo.image[::2, ::2]
            cfa_img[::2, 1::2,1] = G_at_RB(imgPad, (0,1))
            cfa_img[1::2,::2 ,1] = G_at_RB(imgPad, (1,0))
            cfa_img[1::2,1::2,1] = ImageInfo.image[1::2,1::2]
            # R
            cfa_img[::2, ::2 ,0] = RB_at_column(imgPad, (0,0))
            cfa_img[::2, 1::2,0] = RB_at_BR(imgPad, (0,1))
            cfa_img[1::2,::2 ,0] = ImageInfo.image[1::2,::2]
            cfa_img[1::2,1::2,0] = RB_at_row(imgPad, (1,1))
            # B
            cfa_img[::2, ::2 ,2] = RB_at_row(imgPad, (0,0))
            cfa_img[::2, 1::2,2] = ImageInfo.image[::2, 1::2]
            cfa_img[1::2,::2 ,2] = RB_at_BR(imgPad, (1,0))
            cfa_img[1::2,1::2,2] = RB_at_column(imgPad, (1,1))

        case 'GRBG':
            # G
            cfa_img[::2, ::2 ,1] = ImageInfo.image[::2, ::2]
            cfa_img[::2, 1::2,1] = G_at_RB(imgPad, (0,1))
            cfa_img[1::2,::2 ,1] = G_at_RB(imgPad, (1,0))
            cfa_img[1::2,1::2,1] = ImageInfo.image[1::2,1::2]
            # R
            cfa_img[::2, ::2 ,0] = RB_at_row(imgPad, (0,0))
            cfa_img[::2, 1::2,0] = ImageInfo.image[::2, 1::2]
            cfa_img[1::2,::2 ,0] = RB_at_BR(imgPad, (1,0))
            cfa_img[1::2,1::2,0] = RB_at_column(imgPad, (1,1))
            # B
            cfa_img[::2, ::2 ,2] = RB_at_column(imgPad, (0,0))
            cfa_img[::2, 1::2,2] = RB_at_BR(imgPad, (0,1))
            cfa_img[1::2,::2 ,2] = ImageInfo.image[1::2,::2]
            cfa_img[1::2,1::2,2] = RB_at_row(imgPad, (1,1))
            
    outputImageInfo = copy.deepcopy(ImageInfo)
    outputImageInfo.image = np.clip(cfa_img/ 2**ImageInfo.bitNumber, 0, 1).astype(np.float16)
    outputImageInfo.domain = 'RGB'
    outputImageInfo.bayerPattern = None
    outputImageInfo.bitNumber = -1 # bitNumber == -1 means the grayscale in (0,1)
    return outputImageInfo