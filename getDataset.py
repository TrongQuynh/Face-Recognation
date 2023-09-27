import cv2
import os

face_cascaded = cv2.CascadeClassifier(
    "./config/haarcascade_frontalface_default.xml")


def get_data(folder_name):
    count = 0
    count2 = 15
    arr = str(folder_name).split("-")
    user_ID = str(arr[1])
    user_name = str(arr[0])
    print(folder_name)
    is_start_get_dataset = False

    capture = cv2.VideoCapture(2)
    # capture = cv2.VideoCapture("output.mp4")

    while (True):
        isOpened = capture.isOpened()
        if not isOpened:
            capture.open()
        _, frame = capture.read()

        # Convert img from 3D -> 2D
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascaded.detectMultiScale(gray, 1.3, 5)
        new_frame = []
        for (x, y, W, h) in faces:
            x1 = x
            y1 = y
            x2 = x1 + W
            y2 = y1 + h
            cv2.rectangle(img=frame, pt1=(x1, y1), pt2=(
                x2, y2), color=(0, 255, 0), thickness=4)

            # frame[:W, :h] = frame[y1:y2, x1:x2]
            new_frame = gray[y1:y2, x1:x2].copy()

        centerH = frame.shape[0] // 2
        centerW = frame.shape[1] // 2
        sizeboxW = 300
        sizeboxH = 400
        cv2.rectangle(frame, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                      (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

        key = cv2.waitKey(delay=1)

        if key == ord('s'):
            is_start_get_dataset = True
        if is_start_get_dataset:
            if count < 100 and len(new_frame) > 0:
                if not os.path.isdir(f"./data/dataset/{folder_name}"):
                    # create new Folder
                    os.mkdir(f"./data/dataset/{folder_name}")
                cv2.imwrite(
                    f"./data/dataset/{folder_name}/{user_ID}_{count}.jpg", new_frame)
                print("Save pic: " + str(count))
                count += 1

        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f"Number: {count}", (50, 50),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (52, 58, 235), 1)

        cv2.imshow("Form", frame)

        # key = cv2.waitKey(delay=1)
        if key == ord('q') or key == 27:
            break

    capture.release()
    cv2.destroyAllWindows()


get_data("NongTrongQuynh-1669858345")
