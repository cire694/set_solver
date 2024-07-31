import cv2
import numpy as np

# Define the HSV range for each color
color_ranges = {
    'Red': [(0, 70, 50), (15, 255, 255)],
    'Green': [(30, 50, 50), (85, 255, 255)],
    'Purple': [(125, 30, 50), (160, 255, 255)]
}


#pass in a loaded image
def detect_color(image):
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    for index, (color, (lower, upper)) in enumerate(color_ranges.items()):
        mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
        result = cv2.bitwise_and(image, image, mask=mask)
        
        # Check if the mask has enough non-zero values
        if np.count_nonzero(mask) > 1000:
            return color, index
    
    return "Unknown", -1

# Test the function with the uploaded images
image_paths = ['../data/cropped/1111/0.jpg', '../data/cropped/2311/0.jpg', '../data/cropped/3212/2.jpg']

# for path in image_paths:
#     color = detect_color(path)
#     print(f"The detected color in {path} is {color}")
#     image = cv2.imread(path)
#     cv2.imshow(path, image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
