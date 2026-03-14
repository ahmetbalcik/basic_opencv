import cv2

image = cv2.imread("insanlar.jpg")

small = cv2.resize(image, None, fx=0.5, fy=0.5)

cv2.imshow("Resized", small)
cv2.waitKey(0)
cv2.destroyAllWindows()