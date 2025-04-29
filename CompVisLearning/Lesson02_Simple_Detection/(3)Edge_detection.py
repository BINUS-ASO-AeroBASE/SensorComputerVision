# There are multiple edge detection method
# The method that will be used will be Canny edge detection

import cv2
import numpy as np

img = cv2.imread(r"CompVisLearning\Lesson02_Simple_Detection\Image of a lion.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
edges = cv2.Canny(blur, 50, 220)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    print("Amount of edges", len(c))

cv2.imshow("Edges", edges)
cv2.waitKey(0)