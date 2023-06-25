import os.path
import time

import cv2 as cv
import numpy as np
import winsound
from PIL import Image, ImageDraw, ImageFont

from Djiango.settings import BASE_DIR

from interface.code.voice import play_voice

cascade_path = r"C:\FZH\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml"
face_detect = cv.CascadeClassifier(cascade_path)

recognizer = cv.face.LBPHFaceRecognizer_create()


def train(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_coord = face_detect.detectMultiScale(gray)
    x, y, w, h = faces_coord[0]
    # img_cp = img.copy()
    # cv.rectangle(img_cp, (x, y), (x + w, y + h), (0, 0, 255), 10)
    # img_cp = cv.resize(img_cp, (700, 524))
    # cv.imshow('result', img_cp)
    # cv.moveWindow('result', 100, 100)
    # if not idnum:
    # idnum = cv.waitKey(0)
    # cv.destroyWindow('result')
    # if ord('0') < idnum <= ord('9'):
    #     idnum -= 48
    #     faces.append(gray[y:y + h, x:x + w])
    #     ids.append(idnum)
    # if faces:
    recognizer.train([gray[y:y + h, x:x + w]], np.array([1]))
    recognizer.save(os.path.join(BASE_DIR, 'interface/code/trainner/trainner.yml'))


def camera_face(capture):
    cap = cv.VideoCapture(capture)
    while True:
        flag, img = cap.read()
        if not flag:
            break
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces_coord = face_detect.detectMultiScale(gray)
        for x, y, w, h in faces_coord:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv.imshow('camera', img)
        k = cv.waitKey(1)
        if k == ord('0'):
            break
        elif k == ord('+'):
            k = cv.waitKey(0)
            if k == ord('+'):
                train(img)
    cv.destroyAllWindows()
    cap.release()


def file_face(path):
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_coord = face_detect.detectMultiScale(gray)
    # img_cp = img.copy()
    if len(faces_coord) == 0:
        return '未检测到人脸，请重试'
    elif len(faces_coord) > 1:
        return '人脸检测失败，请重试'
    # for x, y, w, h in faces_coord:
        # cv.rectangle(img_cp, (x, y), (x + w, y + h), (0, 0, 255), 10)
    # img_cp = cv.resize(img_cp, (700, 524))
    # cv.imshow('image', img_cp)
    # cv.moveWindow('image', 100, 100)
    # k = cv.waitKey(0)
    # cv.destroyWindow('image')
    # if k == ord('+'):
    train(img)
    return '人脸检测成功'


orders = ['初始', '消费者A', '消费者B', '消费者C', '消费者D', '消费者E']


def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)


def camera_recog(capture):
    cap = cv.VideoCapture(capture)
    recognizer.read(os.path.join(BASE_DIR, 'interface/code/trainner/trainner.yml'))
    start = time.time()
    bl = False
    while True:
        flag, img = cap.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces_coord = face_detect.detectMultiScale(gray)
        for x, y, w, h in faces_coord:
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 150:
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # idn = orders[idnum]
                confidence = int(confidence)
                # img = cv2AddChineseText(img, str(idn), (x + 5, y - 35), (0, 191, 255), 30)
                img = cv2AddChineseText(img, str(confidence), (x + 5, y + h - 35), (0, 191, 255), 30)
            if confidence < 50:
                cv.imshow('camera', img)
                play_voice('人脸识别通过')
                bl = True
        cv.imshow('camera', img)
        if bl:
            break
        now = time.time()
        if now - start > 10:
            cv.destroyAllWindows()
            play_voice('警报')
            winsound.Beep(440, 2000)
            break
        k = cv.waitKey(1)
        if k == ord('0'):
            break
    cv.destroyAllWindows()
    cap.release()


def file_recog(path):
    os.path.join(BASE_DIR, 'interface/code/trainner/trainner.yml')
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_coord = face_detect.detectMultiScale(gray)
    for x, y, w, h in faces_coord:
        idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if confidence < 85:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 10)
            # idn = orders[idnum]
            confidence = "{}%".format(round(100 - confidence))
            # img = cv2AddChineseText(img, str(idn), (x + 5, y - 35), (0, 191, 255), 300)
            img = cv2AddChineseText(img, str(confidence), (x + 5, y + h - 35), (0, 191, 255), 300)
    img_cp = cv.resize(img, (700, 524))
    cv.imshow('image', img_cp)
    cv.moveWindow('image', 100, 100)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    # re = file_face(r'C:\Users\fzhxx\PycharmProjects\TIAS\static\image'
    #                r'\tmp_4c3fec6a6a51ccb385d7015e4c7b8a3c2bae24ac91c80c45.jpg')
    # print(re)
    camera_recog(1)

