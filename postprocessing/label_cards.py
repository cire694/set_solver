import cv2 as cv
import numpy as np
import os 

from keras.models import load_model
from keras_preprocessing.image import load_img
from PIL import Image

from detect_color import detect_color
from find_sets import set_field, card

# redo 2313, 2311, 2322, 2332 (25), 3113 (22), 3133(25), 3211 (THE ENTIRE FOLDER :SKULL:), 3221, 3222, 3311
# remember to chainge from most compatible images

color_index = {
    (255, 0, 0), 
    (0, 0, 255),
    (255, 0, 255)
}

def enlarge_box(box, scale=1.1):
    center = np.mean(box, axis=0)
    new_box = (box - center) * scale + center
    return np.intp(new_box)

def find_sets(img):

    if isinstance(img, str):
        img = cv.imread(img)

    if img is None:
        print(f"Error: Could not open image.")
        return 
    
    
    gray_img, gray_img_contours = gray_img_convert(img)
    
    contours = canny(gray_img)

    filtered_contours = []
    filtered_box = []
    for contour in contours: 
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.intp(box) # turning from floating-point into ints
        
        # area + ratio filtering
        width = rect[1][0]
        height = rect[1][1]

        area = width * height

        ratio = height / width if width != 0 else 0
        
        
        if area > 80000 and  0.5 <= ratio <= 2:

            filtered_contours.append(contour)
            filtered_box.append((rect, box))
        

    filtered_contour_img = cv.drawContours(
        image = img.copy(), 
        contours = [b[1] for b in filtered_box], 
        contourIdx = -1, 
        color = (0, 255, 0), 
        thickness = 3, 
        lineType = cv.LINE_AA
    )

    
    cards = []
    for rect, box in filtered_box:
        width = int(rect[1][0])
        height = int(rect[1][1])

        print("checkpoint")
        dst_pts = np.array([
            [0, height - 1],
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
        ], dtype = "float32")

        M = cv.getPerspectiveTransform(box.astype("float32"), dst_pts)

        warped = cv.warpPerspective(img, M, (width, height))

        if height > width:
            warped = cv.rotate(warped, cv.ROTATE_90_CLOCKWISE)

        pred = predict(warped)
        
        cards.append(card(*pred[0], box))
        
        label = pred[2]

        cv.putText(filtered_contour_img, label, (int(rect[0][0]), int(rect[0][1])), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3, cv.LINE_AA)
    
    sets = set_field(*cards)
    print(sets)


    color_iter = iter(color_index)
    box_scale = 0.1

    for set in sets.sets:
        color = next(color_iter, (0, 0, 0))
        for c in set: 
            enlarged_box = enlarge_box(c.get_contour(), scale = 1 + box_scale)
            filtered_contour_img = cv.drawContours(
                image = filtered_contour_img,
                contours = [enlarged_box], 
                contourIdx=-1, 
                color=color,
                thickness=10,
                lineType=cv.LINE_AA
            )
        box_scale += 0.1

    # cv.imshow("filtered_contour_img", filtered_contour_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return filtered_contour_img


    
    



def gray_img_convert(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    contours, _ =cv.findContours(
        gray_img, 
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )
    gray_img_contours = cv.drawContours(
        image = gray_img.copy(), 
        contours = contours, 
        contourIdx = -1, 
        color = (255, 0, 0), 
        thickness = 3, 
        lineType = cv.LINE_AA
    )

    return gray_img, gray_img_contours

def canny(gray_img):
    blurred = cv.GaussianBlur(gray_img, (7, 7), 0)
    edges = cv.Canny(blurred, threshold1=50, threshold2=150)

    contours, _ = cv.findContours(
        edges, 
        cv.RETR_EXTERNAL,
        cv.CHAIN_APPROX_SIMPLE
    )

    canny_contours = cv.drawContours(
        image = edges.copy(),
        contours = contours, 
        contourIdx = -1, 
        color = (255, 0, 0), 
        thickness = 3, 
        lineType = cv.LINE_AA
    ) 
    return contours


color_model = load_model('../models/color.keras')
number_model = load_model('../models/number.keras')
symbol_model = load_model('../models/symbol.keras')
shading_model = load_model('../models/shading.keras')

def prep(img):
    img = Image.fromarray(img)
    img = img.resize((200, 150), Image.Resampling.LANCZOS)
    feature = np.array(img) 
    feature = feature.reshape(1, 200, 150, 3)

    return feature / 255.0


    
def predict_number(image):
    pred = number_model.predict(image).argmax()

    if pred == 0:
        return "One", 0
    if pred == 1: 
        return "Two", 1
    else:
        return "Three", 2

def predict_symbol(image):
    pred = symbol_model.predict(image).argmax()

    if pred == 0:
        return "Diamond", 0
    if pred == 1: 
        return "Oval", 1
    else:
        return "Squiggle", 2

def predict_shading(image):
    pred = shading_model.predict(image).argmax()

    if pred == 0:
        return "Empty", 0
    if pred == 1: 
        return "Stripe", 1
    else:
        return "Solid", 2


def predict(img):
    preped_img = prep(img)

    color = detect_color(img)
    number = predict_number(preped_img)
    symbol = predict_symbol(preped_img)
    shading = predict_shading(preped_img)
    
    card_string = str(color[0]) + ' ' + str(number[0]) + ' ' + str(symbol[0]) + ' ' + str(shading[0])

    return [color[0], number[0], symbol[0], shading[0]], [color[1] + 1, number[1] + 1, symbol[1] + 1, shading[1] + 1], card_string




cv.imshow("sets:", find_sets(cv.imread('../misc/set4.jpg')))
cv.waitKey(0)
cv.destroyAllWindows()

