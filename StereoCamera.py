import numpy as np
import cv2
import pcdFileManager
from time import sleep
from matplotlib import pyplot as plt


camL = cv2.VideoCapture(0)
camR = cv2.VideoCapture(1)

retL, imgL = camL.read()
retR, imgR = camR.read()

num_rows, num_cols = imgL.shape[:2]

ksize = 41

cloud = []
while True:
    retL, imgL = camL.read()
    retR, imgR = camR.read()

    blurL = cv2.GaussianBlur(imgL, (ksize, ksize), 0)
    blurR = cv2.GaussianBlur(imgR, (ksize, ksize), 0)
    filteredL = imgL - blurL
    filteredR = imgR - blurR
    filteredL = filteredL + 127*np.ones(blurL.shape, np.uint8)
    filteredR = filteredR + 127*np.ones(blurR.shape, np.uint8)
    edgeR = cv2.Canny(imgR,100,100)
    
    dept = 0
    if dept < 0:
            translation_matrix = np.float32([[1, 0, -dept], [0, 1, 0]])
            filteredR = cv2.warpAffine(filteredR, translation_matrix, (num_cols, num_rows))
            dept = 0

    while dept < 15:

        translation_matrix = np.float32([[1, 0, dept], [0, 1, 0]])
        img_translation = cv2.warpAffine(filteredL, translation_matrix, (num_cols, num_rows))
        # disparity = stereo.compute(filteredR, img_translation)
        disparity = cv2.compare(filteredR, img_translation, cv2.CMP_EQ)
        # disparity = cv2.subtract(filteredR, img_translation)
        # cv2.imshow('frame', disparity)
        cv2.imshow('imgL', edgeR)
        # cv2.imshow('imgR', imgR)

        cloud = pcdFileManager.map_one_frame(disparity, imgR, filteredR, dept, cloud)
        
        dept += 1
   # cloud.append((255, 255, 255))
    pcdFileManager.view_map(cloud)



