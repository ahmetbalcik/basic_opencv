import cv2
import numpy as np

image = cv2.imread("insanlar.jpg")
height, weight = image.shape[:2]
rotationMatrix = cv2.getRotationMatrix2D((weight / 2, height / 2), 315, 1.0)
rotationed = cv2.warpAffine(image, rotationMatrix, (weight, height))
cv2.imshow("Rotationed Image", rotationed)
cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()