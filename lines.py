import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math

font = cv2.FONT_HERSHEY_SIMPLEX

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = (255, 255, 255)
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines, thickness, mode):
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8
    )
    if mode == 1:
        img = np.copy(img)
    elif mode == 2:
        img = line_img

    if lines is None:
        return

    printout = []
    for line in lines:
        for x1, y1, x2, y2, letter, color, ang in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
            printout.extend([letter, str(round(ang, 1))])
        cv2.putText(line_img, (str(printout)),(0,50), font, 1.4,(150,100,150),2,cv2.LINE_AA)

    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

    return img

def steer_line(lines):
    # [left_x_start, max_y, left_x_end, min_y]
    if len(lines) == 2:
        line1 = math.atan2(lines[0][1]-lines[0][3], lines[0][0]-lines[0][2])
        line2 = math.atan2(lines[1][1]-lines[1][3], lines[1][0]-lines[1][2])
        ang_between = line1 + line2
        # print(math.degrees(ang_between))
        line = [(lines[0][0]+lines[1][0])/2, lines[0][1], (lines[0][2]+lines[1][2])/2,
                          lines[0][3], "M", (0, 0, 255)]
        # print(line)
        line.append(90+math.degrees(math.atan2(line[3]-line[1], line[2]-line[0])))
        return line


def get_lines(image):
    """
    An image processing pipeline which will output
    an image with the lane lines annotated.
    """
    height = image.shape[0]
    width = image.shape[1]
    region_of_interest_vertices = [
        (width*0.07, height),
        (width*0.5, height*0.35),
        (width*0.85, height),
    ]

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    np.zeros((height,width,3), np.uint8)
    cannyed_image = cv2.Canny(gray_image, 100, 200)

    cropped_image = region_of_interest(
        cannyed_image,
        np.array(
            [region_of_interest_vertices],
            np.int32
        ),
    )
    mask_image = region_of_interest(
        image,
        np.array(
            [region_of_interest_vertices],
            np.int32
        ),
    )
    # gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # cropped_image = region_of_interest(
    #     gray_image,
    #     np.array(
    #         [region_of_interest_vertices],
    #         np.int32
    #     ),
    # )
    # # np.zeros((height,width,3), np.uint8)
    # cannyed_image = cv2.Canny(cropped_image, 100, 200)
    #
    # cropped_image = cannyed_image


    lines = cv2.HoughLinesP(
        cropped_image,
        rho=6,
        theta=np.pi / 60,
        threshold=160,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=25
    )
    if isinstance(lines, np.ndarray):
        left_line_x = []
        left_line_y = []
        right_line_x = []
        right_line_y = []
        left_line = []
        right_line = []
        for line in lines:
            for x1, y1, x2, y2 in line:
                    slope = float(y2 - y1) / (x2 - x1)
                    # print(slope)
                    if math.fabs(slope) < 0.5:
                        continue
                    if slope <= 0:
                        left_line_x.extend([x1, x2])
                        left_line_y.extend([y1, y2])
                    else:
                        right_line_x.extend([x1, x2])
                        right_line_y.extend([y1, y2])


        min_y = int(image.shape[0]*(3.0/5))
        max_y = int(image.shape[0])

        lines_processed = []

        if not left_line_x == []:
            poly_left = np.poly1d(np.polyfit(left_line_y, left_line_x, deg=1))

            left_x_start = int(poly_left(max_y))
            left_x_end = int(poly_left(min_y))
            left_line = [left_x_start, max_y, left_x_end, min_y, "L", (255, 0, 0)]
            left_line.append(90+math.degrees(math.atan2(left_line[3]-left_line[1], left_line[2]-left_line[0])))
            lines_processed.append(left_line)

        if not right_line_x == []:
            poly_right = np.poly1d(np.polyfit(right_line_y, right_line_x, deg=1))

            right_x_start = int(poly_right(max_y))
            right_x_end = int(poly_right(min_y))
            right_line = [right_x_start, max_y, right_x_end, min_y, "R", (0, 255, 0)]
            right_line.append(90+math.degrees(math.atan2(right_line[3]-right_line[1], right_line[2]-right_line[0])))
            lines_processed.append(right_line)

        steer = steer_line(lines_processed)
        if not steer == None:
            lines_processed.append(steer)

        line_image = draw_lines(image, [lines_processed], 12, 1,)

        return line_image#, cropped_image, mask_image
    else:
        return image
    # elif mode == 2:
    #     print(steer[6])
