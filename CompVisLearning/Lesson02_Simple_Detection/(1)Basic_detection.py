import cv2

# Getting the image
img = cv2.imread(r"CompVisLearning\Lesson02_Simple_Detection\shapes_and_colors.jpg") # Get the image
img = cv2.resize(img, (250,250))

while True:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Gray scale the image
    
    blur = cv2.GaussianBlur(gray, (3,3), 0) 
    thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY) # still wrong
    
    counts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
    img2 = img
    for c in counts:
        cv2.drawContours(img2, [c], -1, (0, 255, 100), 1)
    
    cv2.imshow("Image" ,img) # Showing the original image
    cv2.imshow("Grayscaled", gray) # Showing the grayscaled
    cv2.imshow("Show Countour", img2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break