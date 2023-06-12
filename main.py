import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
offset = 20
imgSize = 300
counter = 0

folder = "Data/ok"
labels = ["dislike", "good_job", "good_luck", "hi", "ok", "peace", "rock", "you"]

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # gave us a white background for our camera
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255

        # Image cropping
        imgCrop = img[y-offset:y + h+offset, x-offset:x +w+ offset]
        imgCropShape = imgCrop.shape

        aspectRatio = h/w

        # Calculate height and width
        if aspectRatio > 1:
            # if height higher than width then gave us a aspect ratio of vertical view and center it
            k = imgSize/h
            wCal = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize-wCal) / 2)
            imgWhite[:, wGap:wCal+wGap] = imgResize
            # this will give us prediction of the image that we created before
            prediction, index = classifier.getPrediction(imgWhite,draw=False)
            #print(prediction, index)
        else:
            # if width is higher than height then gave us a aspect ratio of horizontal view and center it
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            # this will give us prediction of the image that we created before
            prediction, index = classifier.getPrediction(imgWhite,draw=False)

        cv2.rectangle(imgOutput, (x - offset, y - offset - 40),
                      (x - offset + 120, y - offset - 100+ 100), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput,labels[index],(x,y-30), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
        cv2.rectangle(imgOutput, (x-offset,y-offset ), (x+w+ offset, y+h+offset), (255,0,255), 4)

        print(labels[index])
        # this will show the camera
        #cv2.imshow("Camera02", imgCrop)
        #cv2.imshow("Camera03", imgWhite)


    cv2.imshow("Camera01", imgOutput)
    cv2.waitKey(1)
