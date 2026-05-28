import os
import re
import urllib.parse

# Mapping for the few files that were cut off in the raw data
special_cases = {
    "Why Can't I Carry All Th": "Why Can't I Carry All This?",
    "Behind the Iron Curtain (M": "Behind the Iron Curtain",
    "Full Can of Whoop-Ass (Moz": "Full Can of Whoop-Ass",
    "Never Going to Give You ": "Never Going to Give You Up",
    "Fire in the Skag Den (Mo": "Fire in the Skag Den"
}

def clean_filename(filename):
    # Separate name and extension
    name, ext = os.path.splitext(filename)
    
    # URL Decode (%20 to space, etc.)
    name = urllib.parse.unquote(name)
    
    # Remove the 24-character hex hash prefix (e.g., 64f1ce5fbd89d8319726da3f_)
    name = re.sub(r'^[a-f0-9]{24}_', '', name)
    
    # Remove standard character tag trailing suffixes
    name = name.replace(" (Moze)", "")
    name = name.strip()
    
    # Resolve known cut-off names from the raw list
    if name in special_cases:
        name = special_cases[name]
        
    return f"{name}{ext}"

def rename_files():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(folder_path):
        # Target only your image types
        if filename.endswith(('.webp', '.avif')):
            new_name = clean_filename(filename)
            if filename != new_name:
                old_file = os.path.join(folder_path, filename)
                new_file = os.path.join(folder_path, new_name)
                try:
                    os.rename(old_file, new_file)
                    print(f"Renamed: {filename} -> {new_name}")
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")

if __name__ == "__main__":
    rename_files()