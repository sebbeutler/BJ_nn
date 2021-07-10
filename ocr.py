# Import required packages
import cv2
import pytesseract
import numpy as np

# 1303, 692
# [[655, 580], [1349, 568], [135, 933], [1825, 916], [410, 182]]

#points = []
#cv2.setMouseCallback("img", perspective, [img])
def perspective(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONUP):
        cv2.circle(param[0], (x,y), 5, (0,255,0), -1)
        points.append([x,y])
        if len(points) == 4:
            matrix = cv2.getPerspectiveTransform(np.float32(points), np.float32([[0,0], [835,0], [0, 313], [835, 313]]))
            cv2.imshow("img", cv2.warpPerspective(param[0], matrix, (1303, 692)))
            cv2.waitKey(0)
            print(points)
            points.clear()



# read the image to be processed
img = cv2.imread("full.png")

# apply perspective transformation to get a top view of the cards (from a 1920x1080 ss only)
matrix = cv2.getPerspectiveTransform(np.float32([[655, 580], [1350, 580], [135, 1000], [1860, 1000]]), np.float32([[0,0], [440,0], [0, 410], [440, 410]]))
img = cv2.warpPerspective(img, matrix, (440, 410))

img_gray = img.copy()

# remove all the non-white pixels to identify the cards
height, width, channels = img.shape
for x in range(width):
    for y in range(height):
        if sum(img_gray[y,x]) < sum((170,170,170)):
            img_gray[y,x] = (0,0,0)

# find contours of white chunk of pixels
img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
ret, im = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)
contours, hierarchie = cv2.findContours(img_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# returns the original image but only the parts inside the selected contours
mask = np.zeros_like(img)
for contour in contours:
    if cv2.contourArea(contour) > 500:
        cv2.fillPoly(mask, [contour], (255,255,255))

result = cv2.bitwise_and(img, mask)

cv2.imshow("res", result)

cv2.waitKey(0)
cv2.destroyAllWindows()