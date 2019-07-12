import imutils, cv2, sys
import numpy as np
import cv2
from text_detect import to_text

##     plate_ratio = 4.73

def process_img(img, limit):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, limit, 255, cv2.THRESH_BINARY)[1]
    return thresh

def crop_contour(image, box):
    #y, y+h, x, x+w
    return image[box[2]:box[3], box[0]:box[1]]

def to_box(contour, margin):
    xmin, xmax, ymin, ymax = 9999,0,9999, 0

    for c in contour:
        c = c[0]
        if c[0] < xmin:
            xmin = c[0]
        if c[0] > xmax:
            xmax = c[0]
        if c[1] < ymin:
            ymin = c[1]
        if c[1] > ymax:
            ymax = c[1]

    m = int((xmax - xmin)*margin)

    return [xmin-m, xmax+m, ymin-m, ymax+m]

def ratio_a(box):
    return float(box[1]-box[0])/float(box[3]-box[2])

def get_plates(image):
    # image = cv2.imread(sys.argv[1])

    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])
    # and threshold it
    # convert the resized image to grayscale, blur it slightly,
    thresh = process_img(resized, 70)

    # find contours in the thresholded image and initialize the
    # shape detectorcnts[3],
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    output = image.copy()
    plates = []
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)

        if M["m00"]+M["m10"]+M["m01"] > 0:
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")

            epsilon = 0.04*cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,epsilon,True)

            if len(approx) == 4:
                if ratio_a(to_box(approx, 0)) > 4:
                    plates.append(approx)
                    cropped = crop_contour(image, to_box(approx, 0.1))
                    # thresh_crop = process_img(cropped, 110)
                    # cv2.imshow("cropped", cropped)
                    # print(to_text(cropped))

    cv2.drawContours(output, plates, -1, (0, 255, 0), 2)

    return output
    # cv2.imshow("Image", output)
    # cv2.waitKey(0)
