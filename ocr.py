import cv2
import pytesseract
import numpy as np

# 1303, 692
# [[655, 580], [1349, 568], [135, 933], [1825, 916], [410, 182]]

points = []
def perspective(event, x, y, flags, param):
    if (event == cv2.EVENT_LBUTTONUP):
        cv2.circle(param[0], (x,y), 5, (0,255,0), -1)
        points.append([x,y])
        if len(points) == 4:
            matrix = cv2.getPerspectiveTransform(np.float32(points), np.float32([[0,0], [608,0], [0, 608], [608, 608]]))
            cv2.imshow("img", cv2.warpPerspective(param[0], matrix, (608, 608)))
            cv2.waitKey(0)
            print(points)
            points.clear()
            


# read the image to be processed
img = cv2.imread("test2.jpg")
#cv2.imshow("img", img)

#cv2.setMouseCallback("img", perspective, [img])
# apply perspective transformation to get a top view of the cards (from a 1920x1080 ss only)
shift = [0.1,-0.1, -0.1, -0.1]
matrix = cv2.getPerspectiveTransform(np.float32([
    [shift[0]*img.shape[1], 0], 
    [img.shape[1]+shift[1]*img.shape[1], 0],     
    [0, shift[2]*img.shape[0]+img.shape[0]],
    [img.shape[1], shift[3]*img.shape[0]+img.shape[0]]]), 
    np.float32([[0,0], [608,0], [0, 608], [608, 608]]))
img = cv2.warpPerspective(img, matrix, (608, 608))

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

#cv2.imshow("img", result)
cv2.imwrite("res.jpg", result)


cv2.waitKey(0)
cv2.destroyAllWindows()