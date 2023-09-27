import os
import time
import cv2
import shutil

path_dataset = "./data/dataset/"


def renameFolder():
    for folder in os.listdir(path_dataset):
        print(folder + "-" + str(int(time.time())))
        time.sleep(1)
        newName = folder + "-" + str(int(time.time()))
        os.rename(f"{path_dataset}{folder}", f"{path_dataset}{newName}")


def renameFile():
    for folder in os.listdir(f"{path_dataset}"):
        id = (str(folder).split("-"))[1]
        for image in os.listdir(f"{path_dataset}{folder}"):
            newFileName = str(id) + "_" + image
            os.rename(f"{path_dataset}{folder}/{image}",
                      f"{path_dataset}{folder}/{newFileName}")


def delete_dataset(foldername):
    if not os.path.isdir(f"./data/dataset/{foldername}"):
        return
    shutil.rmtree(f"./data/dataset/{foldername}")


def detectFace():
    face_cascaded = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml")

    source_data = "D:/New folder/gt_db/gt_db"
    detination_data = "./data/dataset"

    for folder in os.listdir(detination_data):
        delete_dataset(folder)

    for folder in os.listdir(source_data):
        for image in os.listdir(f"{source_data}/{folder}"):

            img = cv2.imread(f"{source_data}/{folder}/{image}", 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascaded.detectMultiScale(gray, 1.3, 5)
            new_frame = []
            for (x, y, W, h) in faces:
                x1 = x
                y1 = y
                x2 = x1 + W
                y2 = y1 + h
                new_frame = gray[y1:y2, x1:x2].copy()

            print(len(new_frame))
            if (len(new_frame) > 0):
                cv2.namedWindow("Show Image", cv2.WINDOW_NORMAL)
                cv2.imshow("Show Image", mat=new_frame)

                cv2.waitKey(1)
            # continue
                if not os.path.isdir(f"{detination_data}/{folder}"):
                    os.mkdir(f"{detination_data}/{folder}")
                print(f"{detination_data}/{folder}/{image}")
                cv2.imwrite(
                    f"{detination_data}/{folder}/{image}", new_frame)
