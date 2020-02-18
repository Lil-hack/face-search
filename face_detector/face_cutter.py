import time
from threading import Thread

import cv2
import os
import uuid
from mtcnn.mtcnn import MTCNN


def crop_face(img,detector):
    try:
        faces = detector.detect_faces(img)
        print (faces)
        print('')
        for face in faces:
            #img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #roi_gray = gray[y:y+h, x:x+w]
            x=face['box'][0]
            y=face['box'][1]
            w=face['box'][2]
            h=face['box'][3]
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            img = img[y:y + h, x:x + w]
            return img
    except:
        pass



if __name__ == '__main__':

    detector = MTCNN()
    folder='men2'
    i=0
    for list_photos in os.walk('/home/zikboy/Documents/data/{}'.format(folder)):
            for photo in list_photos[2]:
                i=i+1
                if i<100000:
                    img = cv2.imread('/home/zikboy/Documents/data/{}/{}'.format(folder,photo), cv2.COLOR_BGR2GRAY)
                    cropped = crop_face(img, detector)
                    # print (img)
                    # print('')
                    try:
                        norm_face=cv2.resize(cropped, (200, 200),fx=0.3,fy=0.3, interpolation=cv2.INTER_AREA)
                        # norm_face=cv2.normalize(norm_face, norm_face, 0, 255, cv2.NORM_MINMAX)
                        cv2.imwrite(r'{}.jpg'.format(folder,uuid.uuid1()), norm_face)
                    except:
                        pass

        # img = cv2.imread('/home/zikboy/Documents/data/men'.format(18), cv2.COLOR_BGR2GRAY)
        # cropped = crop_face(img, face_detector)
        # cv2.imwrite(r'men/{}.jpg'.format(uuid.uuid1()), cropped)
