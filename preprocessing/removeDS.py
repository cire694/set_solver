import os

def remove_ds_store_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '.DS_Store':
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f'Removed: {file_path}')
                except Exception as e:
                    print(f'Error removing {file_path}: {e}')

# Replace 'your_directory' with the path to the directory you want to clean
directory_to_clean = 'cropped'
remove_ds_store_files(directory_to_clean)
