import imutils, cv2, sys
import numpy as np
import cv2
from text_detect import to_text

# [[ 34 510]]
# [[ 98 510]]
# [[102 501]]
# [[ 42 501]]

def process_img(img, limit):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(gray, limit, 255, cv2.THRESH_BINARY)[1]
    return thresh

def crop_contour(image, box):
    # print(box)
    #y, y+h, x, x+w
    return image[box[2]:box[3], box[0]:box[1]]

def to_box(contour, margin):
    xmin, xmax, ymin, ymax = 9999,0,9999, 0
    # print(contour)
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

image = cv2.imread(sys.argv[1])

# resized = image.copy()
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
# print(ratio)
# and threshold it
# convert the resized image to grayscale, blur it slightly,
thresh = process_img(resized, 70)

# find contours in the thresholded image and initialize the
# shape detectorcnts[3],
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
# print(cnts[0][4])
cnts = imutils.grab_contours(cnts)

# cv2.imshow("Thresh", thresh)
# cv2.waitKey(0)
#loop over the contours
# cnts = [cnts[4]]
output = image.copy()

for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)

    if M["m00"]+M["m10"]+M["m01"] > 0:
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        # shape = detect_shape(c)
        # print('Shape:{}, X:{}, Y:{}'.format(shape, cX, cY))
        # print(c)
        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")

        epsilon = 0.04*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        # print(approx)
        if len(approx) == 4:
            # x1, y1 = approx[0][0][0], approx[0][0][1]
            # x2, y2 = approx[1][0][0], approx[1][0][1]
            #


            # xs = 0
            # ys = 0
            # for cont in approx:
            #     xs += cont[0][0]
            #     ys += cont[0][1]
            #
            # cnt_ratio = (float(ys)/4)/(float(xs)/4)

            if ratio_a(to_box(approx, 0)) > 4:
                cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)
                cropped = crop_contour(image, to_box(approx, 0.1))
                thresh_crop = process_img(cropped, 110)
                cv2.imshow("cropped", cropped)
                print(to_text(cropped))
            # print('hej {} {}'.format(xs*0.25, ys*0.25))
            # print(cnt_ratio)


cv2.imshow("Image", output)
cv2.waitKey(0)
