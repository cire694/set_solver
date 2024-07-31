import os

def rename_sorted_images(input_path):
    files = [f for f in os.listdir(input_path) if f not in ('.', '..') and os.path.isfile(os.path.join(input_path, f))]
    
    sorted_files = sorted(files, key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    
    for idx, filename in enumerate(sorted_files):
        new_filename = f"{idx}.jpg"
        old_file = os.path.join(input_path, filename)
        new_file = os.path.join(input_path, new_filename)
        if filename == '.DS_Store':
            os.remove(old_file)
            print(f"Deleted {old_file}")
        os.rename(old_file, new_file)
        print(f"Renamed {old_file} to {new_file}")

def rename_unsorted_images(input_path):

    files = [f for f in os.listdir(input_path) if f not in ('.', '..') and os.path.isfile(os.path.join(input_path, f))]
    
    for idx, filename in enumerate(files):
        new_filename = f"{idx}.jpg"
        old_file = os.path.join(input_path, filename)
        new_file = os.path.join(input_path, new_filename)
        if filename == '.DS_Store':
            os.remove(old_file)
            print(f"Deleted {old_file}")

        os.rename(old_file, new_file)
        print(f"Renamed {old_file} to {new_file}")

path = "../cropped/3333"
rename_sorted_images(path)
