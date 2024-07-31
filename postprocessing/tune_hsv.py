import cv2
import numpy as np

def nothing(x):
    pass

# 'Red': [(5, 70, 50), (15, 255, 255)],
# 'Green': [(30, 50, 50), (85, 255, 255)],
# 'Purple': [(125, 30, 50), (160, 255, 255)]

# Load the image
# image_path = '../data/cropped/2111/7.jpg'
image_path = '../misc/tweak3.png'
image = cv2.imread(image_path)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a window
cv2.namedWindow('image')

# Create trackbars for color change
cv2.createTrackbar('H_low', 'image', 0, 179, nothing)
cv2.createTrackbar('S_low', 'image', 0, 255, nothing)
cv2.createTrackbar('V_low', 'image', 0, 255, nothing)
cv2.createTrackbar('H_high', 'image', 0, 179, nothing)
cv2.createTrackbar('S_high', 'image', 0, 255, nothing)
cv2.createTrackbar('V_high', 'image', 0, 255, nothing)

# Set default value for trackbars
cv2.setTrackbarPos('H_low', 'image', 35)
cv2.setTrackbarPos('S_low', 'image', 50)
cv2.setTrackbarPos('V_low', 'image', 50)
cv2.setTrackbarPos('H_high', 'image', 85)
cv2.setTrackbarPos('S_high', 'image', 255)
cv2.setTrackbarPos('V_high', 'image', 255)

while(1):
    # Get current positions of the trackbars
    h_low = cv2.getTrackbarPos('H_low', 'image')
    s_low = cv2.getTrackbarPos('S_low', 'image')
    v_low = cv2.getTrackbarPos('V_low', 'image')
    h_high = cv2.getTrackbarPos('H_high', 'image')
    s_high = cv2.getTrackbarPos('S_high', 'image')
    v_high = cv2.getTrackbarPos('V_high', 'image')
    
    # Create HSV range arrays
    lower_hsv = np.array([h_low, s_low, v_low])
    upper_hsv = np.array([h_high, s_high, v_high])
    
    # Threshold the HSV image to get only desired colors
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(image, image, mask=mask)
    
    # Show the result
    cv2.imshow('image', result)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # Press 'ESC' to exit
        break

cv2.destroyAllWindows()
