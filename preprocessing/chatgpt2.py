import cv2 as cv
import numpy as np
import os

def detect_card(image_path):
    img = cv.imread(image_path)

    if img is None: 
        print(f"Unable to open image at {image_path}")
        return

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Define the white color range for thresholding
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])

    # Threshold the image to get only white colors
    mask = cv.inRange(hsv, lower_white, upper_white)

    # Use morphological operations to close small gaps in edges
    kernel = np.ones((3, 3), np.uint8)
    morph = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # Find contours
    contours, hierarchy = cv.findContours(
        morph, 
        cv.RETR_EXTERNAL, 
        cv.CHAIN_APPROX_SIMPLE
    )

    card_contour = None
    img_height, img_width = img.shape[:2]
    for contour in contours: 
        area = cv.contourArea(contour)
        x, y, w, h = cv.boundingRect(contour)

        # Filter out the image border by checking the size and position of the contour
        if area > 1000 and w < img_width * 0.9 and h < img_height * 0.9:
            aspect_ratio = float(w) / h
            if 1.0 < aspect_ratio < 2.0:  # Example aspect ratio condition for a card
                card_contour = contour
                break

    if card_contour is not None:
        img_contours = cv.drawContours(image=img.copy(),
                                       contours=[card_contour], 
                                       contourIdx=-1,
                                       color=(255, 0, 0),
                                       thickness=3,
                                       lineType=cv.LINE_AA)
        
        cv.imshow(image_path, img_contours)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("No card detected")


input_folder = '../data/1111/'

for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)

    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.HEIC')):
        detect_card(file_path)