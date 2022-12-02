
import cv2
import os
import numpy as np
import dlib
import time
# Load the detector
face_cascaded = cv2.CascadeClassifier(
    "./config/haarcascade_frontalface_default.xml")

# Call the trained model yml file to recognize faces
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./data/tranning/training.yml")


def get_info_employee(dataset_name): pass


def run():
    start_time = 0
    names = {}  # {1668383566: 'NongTrongQuynh-1668383566'}

    for user in os.listdir("./data/dataset/"):
        id = int(os.listdir(f"./data/dataset/{user}")[0].split('_')[0])
        names[id] = user

    # capture = cv2.VideoCapture("output2.webm")
    # capture = cv2.VideoCapture("output.mp4")

    capture = cv2.VideoCapture(2)

    while (True):
        _, frame = capture.read()
        # Flipping
        # -1: both x-axis and y-axis
        # 0: x-axis
        # 1: y-axis
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascaded.detectMultiScale(gray, 1.3, 5)

        # Flip Image
        # frame = cv2.flip(frame, 1)
        for (x, y, w, h) in faces:
            x1 = x
            y1 = y
            x2 = x1 + w
            y2 = y1 + h
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Prefic and get ID user
            id, confidence = recognizer.predict(gray[y1:y2, x1:x2])

            # confidence_format = f"{int(confidence)} %"
            confidence_format = "  {0}%".format(round(100 - confidence))
            print(id, confidence)
            if (confidence < 70):
                username = str(names[id]).split("-")[0]
            else:
                username = "Unknown"
                # confidence_format = "---"
            cv2.putText(
                frame, username, (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
            cv2.putText(
                frame, confidence_format, (x1, y2), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))

        # Show FPS
        current_time = time.time()
        fps = int(1 / (current_time - start_time))
        start_time = current_time
        cv2.putText(frame, f"FPS: {fps}", (50, 50),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (52, 58, 235), 1)

        cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)

        cv2.imshow("Face Recognition", frame)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


run()
