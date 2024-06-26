import os
import shutil
from datetime import datetime

def move_and_rename_txt_files():
    # Get the current directory and create backup directory path
    current_dir = os.getcwd()
    backup_dir = os.path.join(current_dir, 'DataBackup')
    
    # Create DataBackup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Counter
    moved_count = 0
    
    # Iterate through all files in the current directory
    for filename in os.listdir(current_dir):
        # Check if the file ends with .txt (case-insensitive)
        if filename.lower().endswith('.txt'):
            # Get current timestamp
            current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Create new filename with timestamp
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{current_timestamp}{ext}"
            
            # Define paths
            old_path = os.path.join(current_dir, filename)
            new_path = os.path.join(backup_dir, new_filename)
            
            try:
                # Move and rename the file
                shutil.move(old_path, new_path)
                print(f"Moved and renamed: {filename} -> {new_filename}")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")
    
    # Print results
    if moved_count > 0:
        print(f"\nSuccessfully moved and renamed {moved_count} .txt file(s) to {backup_dir}.")
    else:
        print("\nNo .txt files found in the current directory.")

# Run the function
move_and_rename_txt_files()