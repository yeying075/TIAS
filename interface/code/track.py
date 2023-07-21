import sys
import cv2
import winsound

from interface.code.faceRecognition import camera_recog, camera_recog_2


def track(bbox, capture):
    tk = cv2.TrackerCSRT_create()
    cap = cv2.VideoCapture(capture)
    flag, image = cap.read()
    if not flag:
        print('cannot read video')
        sys.exit()
    # bbox = cv2.selectROI(image, False, False)
    # print(bbox)
    tk.init(image, bbox)
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(image, p1, p2, (255, 0, 0), 2)
    cv2.imshow("Tracking", image)
    while True:
        flag, image = cap.read()
        if not flag:
            break
        flag, bbox = tk.update(image)
        if flag:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(image, p1, p2, (255, 0, 0), 2)
        cv2.imshow("Tracking", image)
        if not flag or p1[0] < 0 or p1[1] < 0 or p2[0] > 640 or p2[1] > 480:
            cv2.destroyAllWindows()
            cap.release()
            print('启动人脸识别')
            camera_recog_2(capture)
            break
        k = cv2.waitKey(1)
        if k == ord('0'):
            break
    cv2.destroyAllWindows()
    cap.release()


# if __name__ == '__main__':
#     track(1, 0)
