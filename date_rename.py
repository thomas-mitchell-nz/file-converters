import os
from PIL import Image
from datetime import datetime

def get_date_taken(path):
    try:
        img = Image.open(path)
        exif_data = img._getexif()
        if exif_data:
            date_taken = exif_data.get(36867)
            if date_taken:
                return datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S').date()
    except Exception as e:
        print(f"Error reading EXIF data for {path}: {e}")
    return None

def rename_photos(directory):
    # Supported file types
    file_types = ['.jpg', '.jpeg', '.png', '.mp4', '.heic', '.JPG', '.JPEG', '.PNG', '.MP4', '.HEIC']  # Add or remove types as needed

    # First pass: Count photos per day, considering file type
    date_counts = {}
    for filename in os.listdir(directory):
        _, ext = os.path.splitext(filename.lower())
        if ext not in file_types:
            continue  # Skip files with extensions not in the supported list

        full_path = os.path.join(directory, filename)
        date_taken = get_date_taken(full_path)
        if date_taken is None:
            continue  # Skip if date cannot be determined

        date_str = date_taken.strftime('%Y%m%d')
        key = (date_str, ext)  # Use a tuple of date and extension as the key
        date_counts[key] = date_counts.get(key, 0) + 1

    # Second pass: Rename photos
    photo_counter = {}
    for filename in os.listdir(directory):
        _, ext = os.path.splitext(filename.lower())
        if ext not in file_types:
            continue

        full_path = os.path.join(directory, filename)
        date_taken = get_date_taken(full_path)
        if date_taken is None:
            continue

        date_str = date_taken.strftime('%Y%m%d')
        key = (date_str, ext)
        photo_counter[key] = photo_counter.get(key, 0) + 1

        # Determine the new name with the original extension
        if date_counts[key] > 1:
            new_name = f"{date_str}_{str(photo_counter[key]).zfill(2)}{ext}"
        else:
            new_name = f"{date_str}{ext}"

        new_full_path = os.path.join(directory, new_name)

        # Rename if the new filename does not exist
        if not os.path.exists(new_full_path):
            os.rename(full_path, new_full_path)
            print(f"Renamed '{filename}' to '{new_name}'")
        else:
            print(f"File {new_full_path} already exists. Skipping...")

# Specify the directory containing your photos
photos_directory = "C:/Users/thoma/Pictures/Photos from 2022"
rename_photos(photos_directory)
