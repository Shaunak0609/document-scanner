import os
from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
from PIL import Image

def scan_document(image_path):
    image = cv2.imread(image_path)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)


    # find the contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # check to see if our approximated contour has four points
        if len(approx) == 4:
            screenCnt = approx
            break

    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    # convert the warped image to grayscale, and using threshold it gives the black and white effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255
    # show the original and scanned images

    cv2.imshow("Original", imutils.resize(orig, height = 650))
    cv2.imshow("Scanned", imutils.resize(warped, height = 650))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    scanned_pil = Image.fromarray(warped)

    # Save as PDF
    scanned_pil.save("your file path")
    print("Saved as scanned_output.pdf")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = ap.parse_args()

if not os.path.exists(args.image):
    raise FileNotFoundError(f"Input image does not exist: {args.image}")

scan_document(args.image)

