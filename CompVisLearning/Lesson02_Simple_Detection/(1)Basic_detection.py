import cv2

# Getting the image
img = cv2.imread(r"CompVisLearning\Lesson02_Simple_Detection\shapes_and_colors.jpg") # Get the image
img = cv2.resize(img, (300,300))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Gray scale the image
    
blur = cv2.GaussianBlur(gray, (3,3), 0) # Blur the image
_, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY) # Changing each pixel to a value of 0 and 1
    
counts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Getting all the countours contained in the image
img2 = img.copy() # Copying the original image so the original image is untouched
for c in counts:
    cv2.drawContours(img2, [c], -1, (0, 255, 100), 2) # Drawing each countour
    # NB: use cv2.approxPolyDP to approximate the countours shape
    
cv2.imshow("Image" ,img) # Show the original image
cv2.imshow("Grayscaled", gray) # Show the grayscaled
cv2.imshow("Show Countour", img2) # Show the image where every shape is drawn
    
cv2.waitKey(0)