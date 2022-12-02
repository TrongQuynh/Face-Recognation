
import cv2
import numpy as np
import os
from PIL import Image


def run():
    name_dirs = []
    paths = []
    detector = cv2.CascadeClassifier(
        "./config/haarcascade_frontalface_default.xml")

    for dir in os.listdir("./data/dataset"):
        print(dir)
        name_dirs.append(dir)

    for name in name_dirs:
        for image in os.listdir(f"./data/dataset/{name}"):
            # path_str = f"dataset/{name}/{image}"
            path_str = os.path.join(f".\data\dataset\{name}", image)

            paths.append(path_str)

    face_store = []
    id_store = []
    # Loop through all img_path in list
    for image_path in paths:

        # Open image in file and convert that img to While and Black
        image = Image.open(image_path).convert("L")

        # Convert that img to matrix using "numpy"
        img_arr = np.array(image, dtype="uint8")
        # Get ID of img from img_path
        tmp_path = str(image_path).replace(".\\", "")
        id = str(tmp_path).split("\\")[3].split("_")[0]

        faces = detector.detectMultiScale(img_arr)
        for (x, y, w, h) in faces:
            face_store.append(img_arr[y:y+h, x:x+w])
            id_store.append(int(id))
        print(str(tmp_path).split("\\")[2])
        img_show = cv2.imread(image_path, 1)
        # cv2.imshow("Show Image", mat=img_show)
        key = cv2.waitKey(1)

    id_store = np.array(id_store)

    # Call the recognizer
    trainer = cv2.face.LBPHFaceRecognizer_create()
    # Give the faces and ids numpy arrays
    trainer.train(face_store, id_store)
    # Write the generated model to a yml file
    trainer.write("./data/tranning/training.yml")
    # trainer.save("./data/tranning/training.yml")
    cv2.destroyAllWindows()


# cv2.destroyAllWindows()
# https: // github.com/chandrikadeb7/Face-Recognition-in -Python/blob/master/2. % 20face % 20training.py
