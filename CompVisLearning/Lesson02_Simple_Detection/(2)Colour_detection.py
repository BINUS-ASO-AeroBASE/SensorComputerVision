import cv2
import numpy as np

img = cv2.imread(r"CompVisLearning\Lesson02_Simple_Detection\shapes_and_colors.jpg")

# Define lower bound and upper bound of blue in HSV (Hue, Saturation and Value)
blue_lower = np.array([100, 70, 70])
blue_upper = np.array([140, 240, 240])

# img = cv2.GaussianBlur(img, (3,3), 0)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
mask = cv2.inRange(img_hsv, blue_lower, blue_upper)
    
countour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in countour:
    cv2.drawContours(img, [c], -1, (0, 255, 100), 2)
    
cv2.imshow("Masked", mask)
cv2.imshow("Masking Blue", img)
cv2.waitKey(0)