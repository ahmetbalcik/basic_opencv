import cv2
import numpy as np

image = cv2.imread("insanlar.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 11, 2)

cv2.imshow("Original", image)
cv2.imshow("Thres1", thresh1)
cv2.imshow("Thres2", thresh2)

cv2.waitKey(0)
cv2.destroyAllWindows()