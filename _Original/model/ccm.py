#!/usr/bin/python
import numpy as np

class CCM:
    'Color Correction Matrix'

    def __init__(self, img, ccm):
        self.img = img
        self.ccm = ccm / 1024.

    # def execute(self):
    #     img_h = self.img.shape[0]
    #     img_w = self.img.shape[1]
    #     img_c = self.img.shape[2]
    #     ccm_img = np.empty((img_h, img_w, img_c), np.uint16)
    #     for y in range(img_h):
    #         for x in range(img_w):
    #             mulval = self.ccm[:,0:3] * self.img[y,x,:]
    #             ccm_img[y,x,0] = np.sum(mulval[0]) + self.ccm[0,3]
    #             ccm_img[y,x,1] = np.sum(mulval[1]) + self.ccm[1,3]
    #             ccm_img[y,x,2] = np.sum(mulval[2]) + self.ccm[2,3]
    #             ccm_img[y,x,:] = ccm_img[y,x,:] 
    #     self.img = ccm_img.astype(np.uint16)
    #     return self.img
    
    def execute(self):
        img_h = self.img.shape[0]
        img_w = self.img.shape[1]
        img_c = self.img.shape[2]
        ccm_img = np.empty(self.img.shape, np.uint16)
        for y in range(img_h):
            for x in range(img_w):
                ccm_img[y,x,:] = np.matmul(self.ccm[:,:3] , self.img[y,x,:]) + self.ccm[:,3]
        self.img = ccm_img.astype(np.uint16)
        return self.img
