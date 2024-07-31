import cv2 as cv
import os

def downsize_image(image_path, output_path):
    # Read the image
    img = cv.imread(image_path)

    if img is None:
        print(f"Unable to open image at {image_path}")
        return

    # Calculate new dimensions
    new_width = int(img.shape[1] * 0.1)
    new_height = int(img.shape[0] * 0.1)
    new_dimensions = (new_width, new_height)

    # Resize the image
    downsized_img = cv.resize(img, new_dimensions, interpolation=cv.INTER_AREA)

    # Save the downsized image
    cv.imwrite(output_path, downsized_img)
    print(f"Saved downsized image to {output_path}")

# Usage

input_folder = '../data/3322'
output_folder = '../data/3322'

for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    if filename == '.DS_Store':
        os.remove(file_path)
        print(f"Deleted {file_path}")

    if filename.lower().endswith(('.png', '.jpg')):
        downsize_image(f"{input_folder}/{filename}", f"{output_folder}/{filename}")