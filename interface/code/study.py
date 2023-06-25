import os
from PIL import Image
import cv2 as cv
import numpy as np

path2 = r"C:\Users\fzhxx\Pictures\23001248_0_final.jpg"
# path = r"C:\Users\fzhxx\Pictures"
# imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
# for imagePath in imagePaths:
#     try:
img = cv.imread(path2)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('image', img)
# cv.waitKey(1000)

print(os.path.split(path2))
print(os.path.split(path2)[-1].split('.')[-1])

# except:
#     pass
