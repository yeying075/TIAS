import sys

import cv2


def track():
    tk_type = 'MIL'
    tk = cv2.TrackerCSRT_create()
    cap = cv2.VideoCapture(1)
    flag, image = cap.read()
    if not flag:
        print('cannot read video')
        sys.exit()
    # bbox = (284, 177, 113, 186)
    bbox = cv2.selectROI(image, False, False)
    # print(bbox)
    tk.init(image, bbox)
    while True:
        flag, image = cap.read()
        if not flag:
            break
        # timer = cv2.getTickCount()
        flag, bbox = tk.update(image)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        fps = cv2.getTickFrequency()
        if flag:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(image, p1, p2, (255, 0, 0), 2, 1)
        cv2.imshow("Tracking", image)
        # Exit
        k = cv2.waitKey(1)
        if k == ord('0'):
            break


if __name__ == '__main__':
    track()
