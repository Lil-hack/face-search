import cv2
import csv
import face_recognition
from mtcnn.mtcnn import MTCNN


if __name__ == '__main__':

    quality_test=1

    if quality_test==1:
        face_cascade = cv2.CascadeClassifier ('detector/haarcascade_frontalface_default.xml')
        count_face=0
        for i in range(1,1000):
            resp = cv2.imread('dataset/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(resp, 1.3, 5, minSize=(30, 30))
            count_face+=len(faces)
            with open('names.csv') as csvfile:
                reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['first_name'], row['last_name'])

        print (count_face)

    if quality_test==2:
        count_face=0
        detector = MTCNN()
        for i in range(1,1000):
            img = cv2.imread('dataset/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
            faces = detector.detect_faces(img)
            count_face+=len(faces)
        print (count_face)

    if quality_test==3:
        count_face = 0
        detector = MTCNN()
        for i in range(1, 1000):
            img = cv2.imread('dataset/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
            faces = face_recognition.face_locations(img)
            count_face += len(faces)
        print(count_face)

