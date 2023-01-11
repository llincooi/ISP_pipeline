#!/usr/bin/python
import numpy as np
import copy
def main(ImageInfo, threshold, mode = 'mean'):
    outputImageInfo = copy.deepcopy(ImageInfo)
    inputImg = ImageInfo.image
    img_pad = np.pad(inputImg, (2, 2), 'reflect').astype(np.int32)

    dpc_img = inputImg.copy()
    for y in range(img_pad.shape[0] - 4):
        for x in range(img_pad.shape[1] - 4):
            p0 = img_pad[y + 2, x + 2]
            p1 = img_pad[y, x]
            p2 = img_pad[y, x + 2]
            p3 = img_pad[y, x + 4]
            p4 = img_pad[y + 2, x]
            p5 = img_pad[y + 2, x + 4]
            p6 = img_pad[y + 4, x]
            p7 = img_pad[y + 4, x + 2]
            p8 = img_pad[y + 4, x + 4]
            differences = p0 - np.array([p1, p2, p3, p4, p5, p6, p7, p8])
            if (differences > 0).all() and (differences < 0).all():    pass
            else: continue
            if (np.abs(differences) > threshold).all():
                match mode:
                    case 'mean':
                        p0 = (p2 + p4 + p5 + p7) / 6 + (p1 + p3 + p6 + p8) / 12
                    case "median":
                        p0 = int(np.median([p1, p2, p3, p4, p5, p6, p7, p8]))
                    case 'nearest':
                        p0 -= differences[np.argmin(np.abs(differences))]
                    case 'gradient':
                        # dv = abs(2 * p0 - p2 - p7)
                        # dh = abs(2 * p0 - p4 - p5)
                        # ddl = abs(2 * p0 - p1 - p8)
                        # ddr = abs(2 * p0 - p3 - p6)
                        dv = np.median( [abs(2 * p0 - p2 - p7), abs(2 * p4 - p1 - p6), abs(2 * p5 - p3 - p8)] )
                        dh = np.median( [abs(2 * p0 - p4 - p5), abs(2 * p2 - p1 - p3), abs(2 * p7 - p6 - p8)] )
                        ddl = np.median( [abs(2 * p0 - p1 - p8), 2* abs(p2 - p5), 2* abs(p4 - p7)] )
                        ddr = np.median( [abs(2 * p0 - p3 - p6), 2* abs(p2 - p4), 2* abs(p5 - p7)] )
                        match np.argmin([dv, dh, ddl, ddr]):
                            case 0:
                                p0 = (p2 + p7) / 2
                            case 1:
                                p0 = (p4 + p5) / 2
                            case 2:
                                p0 = (p1 + p8) / 2
                            case 3:
                                p0 = (p3 + p6) / 2
                dpc_img[y, x] = p0
                
    outputImageInfo.image = dpc_img
    return outputImageInfo
   
# def main(inputImg, threshold, mode = 'mean'):
#     img_pad = np.pad(inputImg, (2, 2), 'reflect').astype(np.int32)

#     dpc_img = inputImg.copy()
#     for y in range(img_pad.shape[0] - 4):
#         for x in range(img_pad.shape[1] - 4):
#             pixels = {"c" : img_pad[y + 2, x + 2],
#                       "1" : img_pad[y, x],
#                       "2" : img_pad[y, x + 2],
#                       "3" : img_pad[y, x + 4],
#                       "4" : img_pad[y + 2, x],
#                       "5" : img_pad[y + 2, x + 4],
#                       "6" : img_pad[y + 4, x],
#                       "7" : img_pad[y + 4, x + 2],
#                       "8" : img_pad[y + 4, x + 4]}
#             differences = pixels['c']- np.array(list(pixels.values())[1:])
#             if ~((differences > 0).all() or (differences < 0).all()):    pass
#             if (np.abs(differences) > threshold).all():
#                 case 'mean':
#                     pixels['c'] = (pixels['2'] + pixels['4'] + pixels['5'] + pixels['7']) / 4
#                 case 'gradient':
#                     dv = abs(2 * pixels['c'] - pixels['2'] - pixels['7'])
#                     dh = abs(2 * pixels['c'] - pixels['4'] - pixels['5'])
#                     ddl = abs(2 * pixels['c'] - pixels['1'] - pixels['8'])
#                     ddr = abs(2 * pixels['c'] - pixels['3'] - pixels['6'])
#                     case == dv):
#                         pixels['c'] = (pixels['2'] + pixels['7']) / 2
#                     case == dh):
#                         pixels['c'] = (pixels['4'] + pixels['5']) / 2
#                     case == ddl):
#                         pixels['c'] = (pixels['1'] + pixels['8']) / 2
#                     else:
#                         pixels['c'] = (pixels['3'] + pixels['6']) / 2
#                 dpc_img[y, x] = pixels['c']
#     return dpc_img

# def main(inputImg, threshold, mode = 'mean'):
#     img_pad = np.pad(inputImg, (2, 2), 'reflect').astype(np.int32)

#     dpc_img = inputImg.copy()
#     for y in range(img_pad.shape[0] - 4):
#         for x in range(img_pad.shape[1] - 4):
#             pixels = img_pad[y:y+5:2, x:x+5:2].flatten()
#             pc = pixels[4]
#             differences = pc - pixels[[0,1,2,3,5,6,7,8]]
#             if ~((differences > 0).all() or (differences < 0).all()):    pass
#             if (np.abs(differences) > threshold).all():
#                 case 'mean':
#                     pc = (pixels[1] + pixels[3] + pixels[5] + pixels[7]) / 4
#                 # case 'gradient':
#                 #     dv = abs(2 * pc - pixels[1] - pixels[7])
#                 #     dh = abs(2 * pc - pixels[3] - pixels[5])
#                 #     ddl = abs(2 * pc - pixels[0] - pixels[8])
#                 #     ddr = abs(2 * pc - pixels[2] - pixels[6])
#                 #     case == dv):
#                 #         pixels['c'] = (pixels['2'] + pixels['7']) / 2
#                 #     case == dh):
#                 #         pixels['c'] = (pixels['4'] + pixels['5']) / 2
#                 #     case == ddl):
#                 #         pixels['c'] = (pixels['1'] + pixels['8']) / 2
#                 #     else:
#                 #         pixels['c'] = (pixels['3'] + pixels['6']) / 2
#                 dpc_img[y, x] = pc
#     return dpc_img