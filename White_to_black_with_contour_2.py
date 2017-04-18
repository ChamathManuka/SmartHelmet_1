from PIL import Image
import numpy as np
import argparse
import cv2
import logging
import os
import re
import six
import operator




cap = cv2.VideoCapture(0)

while(1):
    _, img_rgb = cap.read()
    _, frame = cap.read()
###########################################################################
    _, image1 = cap.read()
    orig = image1.copy()
    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),2)
    blur = cv2.bilateralFilter(gray,9,75,75)

    #gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
    image1 = orig.copy()
    print (maxLoc)
    maxLoc = tuple(map(sum, zip(maxLoc, (20,60))))

    for x in range(5, 60,5):
        
        cv2.circle(image1, maxLoc, x, (0, 0, 0), 3)
############################################################################

    Conv_hsv_Gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
    img_rgb[mask == 0] = [255, 255, 255]
    imgray = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(imgray)
    #print(maxLoc)
    cv2.circle(frame, maxLoc, 60, (255, 0, 0), -1)
    #cv2.imshow("native", frame)


    

    (_, cnts, _) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri,True)

    print(len(approx))
    if len(approx) <= 6:
            screenCnt = approx
            print("chamth")
            kernel = np.ones((8,8),np.uint8)
            erosion = cv2.erode(mask,kernel,iterations = 1)
            opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
            #cv2.imshow("dots", opening)
            (_, cnts_2, _) = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            print("I found %d black shapes" % (len(cnts_2)))

            for z in cnts_2:
                #cv2.drawContours(opening, [z], -1, (0, 255, 0), 2)
                cX=0
                cY=0
                M = cv2.moments(z)
                print(M)
                #cX = int(M["m10"] / M["m00"])
                #cY = int(M["m01"] / M["m00"])
                #cv2.circle(opening, (cX, cY), 14, (255, 255, 255), -1)
                #cv2.putText(opening, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                small = cv2.resize(opening, (0,0), fx=0.5, fy=0.5)
                #image1 = cv2.(image1, (800, 200))

                #cv2.imshow("Image", small)
                #if(maxLoc[0] > 0 & maxLoc[1] > 0):
                    
                crop_img = image1[200:200, 400:800]
                cv2.imshow("Robust", image1)
                cv2.waitKey(0)
    else:
        cv2.destroyWindow("dots")
        cv2.destroyWindow("Image")
        cv2.destroyWindow("Robust")
    #cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)
    #cv2.imshow("Game Boy Screen", frame)
    

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
cap.release()
