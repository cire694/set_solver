import cv2 as cv
import numpy as np
import os 

# redo 2313, 2311, 2322, 2332 (25), 3113 (22), 3133(25), 3211 (THE ENTIRE FOLDER :SKULL:), 3221, 3222, 3311
# remember to chainge from most compatible images
def cropImage(path):
    img = cv.imread(path)

    if img is None: 
        print(f"Unable to open image at {path}")
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
        
        
        if area > 1000 and  0.5 <= ratio <= 2:

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

    cv.imshow("filtered_contour_img", filtered_contour_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    for rect, box in filtered_box:
        width = int(rect[1][0])
        height = int(rect[1][1])


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
            
            cv.imshow(path, warped)
            cv.waitKey(0)
            cv.destroyAllWindows()

    



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





input_path = '../data/3113'

files = os.listdir(input_path)
sorted_files = sorted(files,
                    key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
for filename in sorted_files:

    print(f'{input_path}/{filename}')
    cropImage(f'{input_path}/{filename}')


# input_path = '../data/'
# folders = [folder for folder in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, folder))]

# sorted_folders = sorted(folders, key=lambda x: int(x))

# for folder in sorted_folders:
#     folder_path = os.path.join(input_path, folder)
#     files = [file for file in os.listdir(folder_path) if file != '.DS_Store']
#     sorted_files = sorted(files, key=lambda x: int(os.path.splitext(x)[0]))
    
#     for filename in sorted_files:
#         file_path = os.path.join(folder_path, filename)
        
        
#         print(file_path)
#         cropImage(file_path)
