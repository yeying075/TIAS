import os
import re

import cv2
from cnocr import CnOcr

from TIAS.settings import BASE_DIR
from interface.code.track import track


def camera_text(encodeing, idnum, capture):
    cap = cv2.VideoCapture(capture)
    ocr = CnOcr()
    bl = False
    bbox = ()
    while True:
        flag, img = cap.read()
        if not flag:
            break
        cv2.imwrite(os.path.join(BASE_DIR, 'interface/code/data/textImage.jpg'), img)
        res = ocr.ocr(os.path.join(BASE_DIR, 'interface/code/data/textImage.jpg'))
        for x in res:
            if x['text'].find(idnum) != -1:
                array = x['position']
                position1 = (int(array[0][0])-50, int(array[0][1])-50)
                position2 = (int(array[2][0])+50, int(array[2][1])+100)
                bbox = (position1[0], position1[1], position2[0]-position1[0], position2[1]-position1[1])
                # img = cv2.imread('./data/textImage.jpg')
                # cv2.rectangle(img, position1, position2, (0, 0, 255), 1)
                # cv2.imshow('image', img)
                # cv2.waitKey(0)
                bl = True
        if bl:
            break
        cv2.imshow('camera', img)
        k = cv2.waitKey(1)
        if k == ord('0'):
            break
    cv2.destroyAllWindows()
    cap.release()
    if bl:
        print('检测到外卖')
        track(encodeing, bbox, capture)


def file_text(encodeing, path, capture):
    ocr = CnOcr()
    res = ocr.ocr(path)
    bl2 = False
    bl = False
    i = 1
    k = -1
    for x in res:
        if x['text'].find('订单编号') != -1:
            k = i
        if i == k+1:
            temp = x['text']
            temp = temp.replace(' ', '')
            idnum = re.search('\d+', temp)
            if idnum:
                idnum = idnum.group()
                print(idnum)
                if 10 < len(idnum) < 40:
                    bl = True
                    camera_text(encodeing, idnum, capture)
        i += 1
    if bl:
        return ''
    else:
        return '未识别到订单编号，请重试'


# if __name__ == '__main__':
