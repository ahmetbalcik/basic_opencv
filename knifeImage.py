import cv2
import numpy as np

image = cv2.imread("insanlar.jpg")

kernel = np.array([
    [-1, -1,-1],
    [-1, 9, -1],
    [-1, -1,-1],
])
keen = cv2.filter2D(image, -1, kernel)

cv2.imshow("Original", image)
cv2.imshow("Knife", keen)

cv2.waitKey(0)
cv2.destroyAllWindows()