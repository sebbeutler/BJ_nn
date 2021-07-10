import cv2 as cv

img = cv.imread('test.png')

img_gray = cv.cvtColor(img, cv.COLOR_BGR2HSV)

cv.imwrite('test_hsv.png', img_gray)