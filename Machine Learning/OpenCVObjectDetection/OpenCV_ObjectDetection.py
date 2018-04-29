
import numpy as np
import cv2 as cv
face_cascade = cv.CascadeClassifier('E:/handGesture/aGest.xml')
cap = cv.VideoCapture(0)
#img = cv.imread('E:/handGesture/test.jpg')
listoxPoints=[]
while True:
    ret, img = cap.read()
    #gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 5, 5)
    for (x,y,w,h) in faces:
        listoxPoints.append([x, y])
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    #for p in listoxPoints:
    points = np.array([listoxPoints], np.int32)
    print(points)
    try:
        cv.polylines(img, points, False, (0, 0, 255))
    except:
        pass
        #cv(img, (p[0], p[1]), 2, (255, 0, 0), 2)
    cv.imshow('object detection', cv.resize(img, (400, 300)))
    if cv.waitKey(50) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break
