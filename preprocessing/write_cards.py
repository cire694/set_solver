import cv2 as cv
import numpy as np
import os 

# add: 2311
# remember to chainge from most compatible images
def cropImage(path, output_path):
    img = cv.imread(path)

    if img is None: 
        print(f"Unable to open image at {path}")
        return 
    
    gray_img, gray_img_contours = gray_img_convert(img)
    
    contours = canny(gray_img)

    if not contours: 
        print(f"No contours found in image at {path}")
        return
    
    largest_contour = max(contours, key = cv.contourArea)
    rect = cv.minAreaRect(largest_contour)
    box = cv.boxPoints(rect)
    box = np.intp(box) # turning from floating-point into ints
    
        

    filtered_contour_img = cv.drawContours(
        image = img.copy(), 
        contours = [box], 
        contourIdx = -1, 
        color = (0, 255, 0), 
        thickness = 3, 
        lineType = cv.LINE_AA
    )

    
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
        
    cv.imwrite(output_path, warped)
        

    



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





input_path = '../data/1111'
output_path = '../cropped/1111'

files = [file for file in os.listdir(input_path) if file != '.DS_Store']
sorted_files = sorted(files,
                    key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

os.makedirs(output_path, exist_ok=True)
for filename in sorted_files:

    print(f'{input_path}/{filename}')
    cropImage(f'{input_path}/{filename}', f'{output_path}/{filename}')
# main_input_path = '../data'
# main_output_path = '../cropped'

# subfolders = [f.path for f in os.scandir(main_input_path) if f.is_dir()]

# for subfolder in subfolders:
#     # Define the input and output paths for the current subfolder
#     input_path = subfolder
#     output_path = os.path.join(main_output_path, os.path.basename(subfolder))
    
#     # Get the list of files in the current subfolder
#     files = [file for file in os.listdir(input_path) if file != '.DS_Store']
#     sorted_files = sorted(files, key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    
#     # Create the output directory for the current subfolder
#     os.makedirs(output_path, exist_ok=True)
    
#     for filename in sorted_files:
#         input_file = os.path.join(input_path, filename)
#         output_file = os.path.join(output_path, filename)
        
#         print(f'{input_file}')
#         cropImage(input_file, output_file)
