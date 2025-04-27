import cv2

# Getting the image
img = cv2.imread(r"SensorComputerVision\CompVisLearning\Lesson02_Simple_Detection\shapes_and_colors.jpg")
img = cv2.resize(img, (250,250))

while True:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("Image" ,img)
    cv2.imshow("Grayscaled", gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break