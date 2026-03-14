import cv2
import numpy as np

image = cv2.imread("insanlar.jpg")
blur1 = cv2.blur(image, (15,15))
blur2 = cv2.GaussianBlur(image, (15,15), 0)

cv2.imshow("Original Image", image)
cv2.imshow("Blur", blur1)
cv2.imshow("Gaussian Blur", blur2)
cv2.waitKey(0)
cv2.destroyAllWindows()