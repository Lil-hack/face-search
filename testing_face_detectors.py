import time

import numpy as np
import cv2


face_cascade = cv2.CascadeClassifier ('haarcascade_frontalface_default.xml')
result_time=0
count_face=0
for i in range(19,20):
    resp = cv2.imread('dataset/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
    t0 = time.time()
    faces = face_cascade.detectMultiScale(resp, 1.3, 5, minSize=(30, 30))
    print (faces)
    for (x, y, w, h) in faces:
        r = max(w, h) / 2
        centerx = x + w / 2
        centery = y + h / 2
        nx = int(centerx - r)
        ny = int(centery - r)
        nr = int(r * 2)
        faceimg = resp[ny:ny + nr, nx:nx + nr]
        cv2.imshow('123',faceimg)

    result_time+=time.time()-t0


print(result_time)


result_time=0
count_face=0
for i in range(19,20):
    resp = cv2.imread('dataset/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
    t0 = time.time()
    faces = face_cascade.detectMultiScale(resp, 1.3, 5, minSize=(30, 30))
    print (faces)
    for (x, y, w, h) in faces:
        r = max(w, h) / 2
        centerx = x + w / 2
        centery = y + h / 2
        nx = int(centerx - r)
        ny = int(centery - r)
        nr = int(r * 2)
        faceimg = resp[ny:ny + nr, nx:nx + nr]
        cv2.imshow('123',faceimg)

    result_time+=time.time()-t0


print(result_time)
