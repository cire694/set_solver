import os
from PIL import Image

# Define the path to your dataset
dataset_dir = '../cropped'
# Target size for resizing
target_size = (200, 150)

# Function to resize images in a directory
def resize_images_in_directory(directory, target_size):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('jpg', 'jpeg', 'png', 'bmp', 'gif')):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        img = img.resize(target_size, Image.Resampling.LANCZOS)
                        img.save(file_path)
                    print(f"Resized {file_path}")
                except Exception as e:
                    print(f"Failed to resize {file_path}: {e}")

# Resize images in the dataset directory
resize_images_in_directory(dataset_dir, target_size)

print("Images resized successfully!")
