import cv2, sys
import numpy as np
from text_detect import to_text

#crop sign
def cropContour(image, center, radius, margin):
    radius = int(radius * margin)
    left = center[0]-radius
    right = center[0]+radius
    top = center[1]+radius
    bottom = center[1]-radius
    # print(left, right, top, bottom)
    return image[bottom:top, left:right]
    # return image[left:right, top:bottom]

def detect_shape(img):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

def plate(image):
    # load the image, clone it for output, and then convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, widht, channels = image.shape
    plate_ratio = 4.73

    # # detect circles in the image
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 200, maxRadius=50)
    # print(circles)
    # # ensure at least some circles were found
    # if circles is not None:
    #   # convert the (x, y) coordinates and radius of the circles to integers
    #   circles = np.round(circles[0, :]).astype("int")
    #
    #   # loop over the (x, y) coordinates and radius of the circles
    #   for (x, y, r) in circles:
    #       cv2.circle(image, (x, y), int(r*1.3), (255, 100, 0), 2)
    #   x, y, r = circles[0]
    #   output = cropContour(output, (x, y), r, 1)
    #
    #     # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    #
    #   # show the output image
    #   print("HELLO DIS IS SPEED LIMIT: {}".format(to_text(output).rstrip(")")))
    output = cv2.Canny(gray, 80, 150)

    # output = cv2.resize(output, (int(widht*0.5), int(height*0.5)))
    print("HELLO DIS IS SPEED LIMIT: {}".format(to_text(output).rstrip("")))

    return output

out1 = plate(cv2.imread(sys.argv[1]))
cv2.imshow("Cropped", out1)
# cv2.imshow("Original", out2)
cv2.waitKey(0)
