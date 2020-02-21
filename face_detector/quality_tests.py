import cv2
import csv
import face_recognition
from mtcnn.mtcnn import MTCNN


if __name__ == '__main__':

    quality_test=1

    if quality_test==1:
        face_cascade = cv2.CascadeClassifier ('face_detector/haarcascade_frontalface_default.xml')
        count_face=0
        with open('dataset_haar.csv', 'w') as csvfile:
            fieldnames = ['N', 'Haar']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(1, 1000):
                resp = cv2.imread('dataset_for_tests/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(resp, 1.3, 5, minSize=(30, 30))
                count_face += len(faces)
                writer.writerow({'N': i, 'Haar': len(faces)})

        print (count_face)

    if quality_test==2:
        count_face=0
        detector = MTCNN()
        with open('dataset_tensorflow.csv', 'w') as csvfile:
            fieldnames = ['N', 'MTCNN']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(1, 1000):
                img = cv2.imread('dataset_for_tests/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
                faces = detector.detect_faces(img)
                count_face += len(faces)
                writer.writerow({'N': i, 'MTCNN': len(faces)})

        print (count_face)

    if quality_test==3:
        count_face = 0
        with open('dataset_dlib.csv', 'w') as csvfile:
            fieldnames = ['N', 'Dlib']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(1, 1000):
                img = cv2.imread('dataset_for_tests/face{}.jpg'.format(i), cv2.COLOR_BGR2GRAY)
                faces = face_recognition.face_locations(img)
                count_face += len(faces)
                writer.writerow({'N': i, 'Dlib': len(faces)})

        print(count_face)

