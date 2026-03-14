import cv2
import numpy as np

image = cv2.imread("insanlar.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

cv2.imshow("Original", image)
cv2.imshow("Edges of Image", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()