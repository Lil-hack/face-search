import time
import cv2
import face_recognition
from mtcnn.mtcnn import MTCNN


if __name__ == '__main__':

    speed_test=1

    if speed_test==1:
        face_cascade = cv2.CascadeClassifier ('face_detector/haarcascade_frontalface_default.xml')
        result_time=0
        for i in range(1,1000):
            resp = cv2.imread('dataset_for_tests/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
            t0 = time.time()
            faces = face_cascade.detectMultiScale(resp, 1.3, 5, minSize=(30, 30))
            result_time+=time.time()-t0
            print(faces)
        print(result_time)

    if speed_test==2:
        result_time=0
        detector = MTCNN()
        for i in range(1,1000):
            img = cv2.imread('dataset_for_tests/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
            t0 = time.time()
            faces = detector.detect_faces(img)
            result_time+=time.time()-t0
            print(faces)
        print(result_time)

    if speed_test==3:
        result_time = 0
        for i in range(1, 1000):
            img = cv2.imread('dataset_for_tests/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
            t0 = time.time()
            face_locations = face_recognition.face_locations(img)
            result_time += time.time() - t0
            print(face_locations)
        print(result_time)
