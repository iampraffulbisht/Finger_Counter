import cv2 as cv
import numpy as np
import math
import mediapipe
import hand_tracking_module as htm
import os
import time

wCam, hCam = 1280, 720

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath = "FingerCounting/Fingers"
myList = os.listdir(folderPath)
myList.sort()
print(myList)
overlayList = []
for imgPath in myList:
    image = cv.imread(f'{folderPath}/{imgPath}')
    print(f'{folderPath}/{imgPath}')
    overlayList.append(image)
for i in range(len(overlayList)):
    overlayList[i] = cv.resize(overlayList[i], (200, 200))
specificImage = cv.imread("FingerCounting/f.png")
specificImage = cv.resize(specificImage, (150, 200))
pTime  =0


detector = htm.handDetector(detectionCon=0.75)


tipIds = [4, 8 ,12, 16, 20]

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList)!=0:
        fingers = []
        #thu,b

        
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]: 
                fingers.append(1)
        else:
                fingers.append(0)

        for id in range(1,5):
            
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        
        
        totalFingers = fingers.count(1)

        # print(totalFingers)

        if fingers == [0,0,1,0,0]:
            h, w, c = specificImage.shape
            img[0:h, 0:w] = specificImage
            cv.rectangle(img,(0,225),(350,445),(128,128,128),cv.FILLED)
            cv.putText(img,"Fuck",(35,300),cv.FONT_HERSHEY_COMPLEX_SMALL,5,(0,0,0),5)
            cv.putText(img,"you",(35,400),cv.FONT_HERSHEY_COMPLEX_SMALL,5,(0,0,0),5)
        
        else:
            h,w,c = overlayList[totalFingers-1].shape
            img[0:h, 0:w] = overlayList[totalFingers-1]
            cv.rectangle(img,(0,225),(150,425),(128,128,128),cv.FILLED)
            cv.putText(img,str(totalFingers),(35,375),cv.FONT_HERSHEY_PLAIN,10,(255,0,0),10)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img,f'FPS:{int(fps)}',(1100,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv.imshow("Webcam",img) 
    if cv.waitKey(15) & 0xFF == ord('q'):
        break

