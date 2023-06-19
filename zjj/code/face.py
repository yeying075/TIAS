import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

cascade_path = r"C:\FZH\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml"
face_detect = cv.CascadeClassifier(cascade_path)

recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read('trainner/trainner.yml')

cap = cv.VideoCapture(0)


def train(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_coord = face_detect.detectMultiScale(gray)
    faces = []
    ids = []
    for x, y, w, h in faces_coord:
        img_cp = img.copy()
        cv.rectangle(img_cp, (x, y), (x + w, y + h), (0, 0, 255), 10)
        img_cp = cv.resize(img_cp, (700, 524))
        cv.imshow('result', img_cp)
        cv.moveWindow('result', 100, 100)
        # if not idnum:
        idnum = cv.waitKey(0)
        cv.destroyWindow('result')
        if ord('0') < idnum <= ord('9'):
            idnum -= 48
            faces.append(gray[y:y + h, x:x + w])
            ids.append(idnum)
    if faces:
        recognizer.train(faces, np.array(ids))
        recognizer.save('trainner/trainner(2).yml')


def camera_add():
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
            train(img)
    cv.destroyWindow('camera')


def file_add(path):
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_coord = face_detect.detectMultiScale(gray)
    img_cp = img.copy()
    for x, y, w, h in faces_coord:
        cv.rectangle(img_cp, (x, y), (x + w, y + h), (0, 0, 255), 10)
    img_cp = cv.resize(img_cp, (700, 524))
    cv.imshow('image', img_cp)
    cv.moveWindow('image', 100, 100)
    k = cv.waitKey(0)
    cv.destroyWindow('image')
    if k == ord('+'):
        train(img)


orders = ['初始', '方子豪', '张芝轩', 'B', 'C', 'D']


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


def camera_recog():
    while True:
        flag, img = cap.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces_coord = face_detect.detectMultiScale(gray)
        for x, y, w, h in faces_coord:
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence < 85:
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                idn = orders[idnum]
                confidence = int(confidence)
                img = cv2AddChineseText(img, str(idn), (x + 5, y - 35), (0, 191, 255), 30)
                img = cv2AddChineseText(img, str(confidence), (x + 5, y + h - 35), (0, 191, 255), 30)
        cv.imshow('camera', img)
        k = cv.waitKey(1)
        if k == ord('0'):
            break
    cv.destroyWindow('camera')


def file_recog(path):
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces_coord = face_detect.detectMultiScale(gray)
    for x, y, w, h in faces_coord:
        idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if confidence < 85:
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 10)
            idn = orders[idnum]
            confidence = "{}%".format(round(100 - confidence))
            img = cv2AddChineseText(img, str(idn), (x + 5, y - 35), (0, 191, 255), 300)
            img = cv2AddChineseText(img, str(confidence), (x + 5, y + h - 35), (0, 191, 255), 300)
    img_cp = cv.resize(img, (700, 524))
    cv.imshow('image', img_cp)
    cv.moveWindow('image', 100, 100)
    cv.waitKey(0)
    cv.destroyWindow('image')

