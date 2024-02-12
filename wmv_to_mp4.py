import ffmpeg
import os
import subprocess
import json

def get_creation_time(source_path):
    """Extracts the creation time from the video file using ffprobe."""
    try:
        # Use ffprobe to extract video metadata as JSON
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format_tags=creation_time", "-of", "json", source_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        # Parse the JSON output
        metadata = json.loads(result.stdout)
        # Extract the creation time
        creation_time = metadata["format"]["tags"]["creation_time"]
        return creation_time
    except Exception as e:
        print(f"Error extracting creation time from {source_path}: {e}")
        return None

def convert_wmv_to_mp4_with_metadata(source_folder, target_folder=None):
    if target_folder is None:
        target_folder = source_folder
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    for filename in os.listdir(source_folder):
        if filename.endswith(".wmv") or filename.endswith(".WMV"):
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename[:-4] + '.mp4')
            
            try:
                # Extract the creation time from the source file
                creation_time = get_creation_time(source_path)
                
                # Convert .wmv to .mp4 and set creation_time if available
                if creation_time:
                    ffmpeg.input(source_path).output(target_path, metadata='creation_time=' + creation_time).run(overwrite_output=True)
                else:
                    ffmpeg.input(source_path).output(target_path).run(overwrite_output=True)
                
                print(f"Converted {filename} to {filename[:-4] + '.mp4'} successfully.")
            except ffmpeg.Error as e:
                print(f"Error converting {filename}: {e}")
                
if __name__ == "__main__":
    source_folder = 'file-converters/wmv'
    target_folder = 'file-converters/mp4'
    convert_wmv_to_mp4_with_metadata(source_folder, target_folder)
