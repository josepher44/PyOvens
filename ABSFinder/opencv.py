"""
Simply display the contents of the webcam with optional mirroring using OpenCV
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import cv2 as cv2
import numpy as np


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(1)
    while True:
        ret_val, img = cam.read()
        img = img[200:400, 200:400]
        blurred = cv2.pyrMeanShiftFiltering(img,31,61)
        grayscaled = cv2.cvtColor(blurred,cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 5)

        edges = cv2.Canny(thresh,100,200)

        kernel = np.ones((5,5), np.uint8)
        img_dilation = cv2.dilate(edges, kernel, iterations=1)
        #img_dilation2 = cv2.dilate(edges, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        print(len(contours))
        try:
            cnt=contours[0]
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(img,[box],0,(0,0,255),2)
            #cv.drawContours(thresh, contours, -1(0,0,255),6)

            center, size, theta = rect
            center, size = tuple(map(int, center)), tuple(map(int, size))
            M = cv2.getRotationMatrix2D( center, theta, 1)
            dst = cv2.warpAffine(img, M, img.shape[:2])
            out = cv2.getRectSubPix(dst, size, center)
            length, width = size
            slength = length*3
            swidth = width*3
            outscale = cv2.resize(out, (slength,swidth))


            cv2.imshow('thresh', thresh)
            cv2.imshow('canny', edges)
            cv2.imshow('edges', img_dilation)
            #cv2.imshow('dilation', img_dilation2)
            cv2.imshow('original', img)
            cv2.imshow('croprotate', outscale)
        except:
            print("no object")
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=False)


if __name__ == '__main__':
    main()
