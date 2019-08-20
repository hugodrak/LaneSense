import imutils, cv2, sys
import numpy as np
import cv2
from text_detect import to_text

##     plate_ratio = 4.73


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = (255, 255, 255)
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

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

    # masked_image = imutils.resize(image, width=300)


    height = image.shape[0]
    width = image.shape[1]

    region_of_interest_vertices = [
            (width*0.0, height),
            (width*0.0, height*0.65),
            (width*0.32, height*0.45),
            (width*0.5, height*0.45),
            (width*0.8, height*0.9),
            (width*0.8 , height),
    ]

    masked_image = region_of_interest(
        image,
        np.array(
            [region_of_interest_vertices],
            np.int32
        ),
    )


    ratio = image.shape[0] / float(masked_image.shape[0])
    # and threshold it
    # convert the masked_image image to grayscale, blur it slightly,
    thresh = process_img(masked_image, 70)

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
                box = to_box(approx, 0)
                widht = box[1]-box[0]

                #if the ratio of the detected box is grater than 4 between widht and height and if the widht exceeds 30 pixels(regplate)
                if ratio_a(box) > 4 and widht > 29:
                    plates.append(approx)
                    cropped = crop_contour(image, to_box(approx, 0.1))
                    # thresh_crop = process_img(cropped, 110)
                    # cv2.imshow("cropped", cropped)
                    # print(to_text(cropped))
    print(len(plates))
    print(type(thresh), type(output))
    cv2.drawContours(thresh, plates, -1, (0, 255, 0), 2)

    return thresh
