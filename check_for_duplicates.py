import os

def find_duplicate_filenames(folder_path):
    # Dictionary to store filenames without extension as keys
    # and lists of corresponding file paths as values
    filenames_dict = {}

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        # Get the filename without extension
        filename_without_extension = os.path.splitext(filename)[0]
        # If filename exists in the dictionary, append the filepath
        if filename_without_extension in filenames_dict:
            filenames_dict[filename_without_extension].append(os.path.join(folder_path, filename))
        else:
            filenames_dict[filename_without_extension] = [os.path.join(folder_path, filename)]

    # Filter out filenames with more than one filepath (duplicates)
    duplicate_filenames = {filename: filepaths for filename, filepaths in filenames_dict.items() if len(filepaths) > 1}

    return duplicate_filenames

if __name__ == "__main__":
    folder_path = input("Enter the path of the folder: ")
    duplicate_filenames = find_duplicate_filenames(folder_path)
    if duplicate_filenames:
        print("Duplicate filenames found:")
        for filename, filepaths in duplicate_filenames.items():
            print(f"Filename: {filename}, Filepaths: {filepaths}")
    else:
        print("No duplicate filenames found in the folder.")
