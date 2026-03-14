import cv2

image = cv2.imread("insanlar.jpg")

if image is None:
    print("Image Not Found!")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Screen Gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()