import os
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the source and destination directories
source_dir = os.getenv('SOURCE_DIR')
destination_dir = './Inbox'

# List of files to move
files_to_move = [
    '2020-2021 Season.xlsx',
    '2021-2022 Season.xlsx',
    '2022-2023 Season.xlsx',
    '2023- 2024 Season.xlsx',
    '2024- 2025 Season.xlsx'
]

# Ensure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Move each file from the source directory to the destination directory
for file_name in files_to_move:
    source_file = os.path.join(source_dir, file_name)
    destination_file = os.path.join(destination_dir, file_name)
    
    try:
        if os.path.exists(destination_file):
            print(f"File already exists and will not be overwritten: {file_name}")
        else:
            shutil.move(source_file, destination_file)
            print(f"Moved: {file_name}")
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error moving {file_name}: {e}")