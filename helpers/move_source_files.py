import os
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the source and destination directories
source_dir = os.getenv('SOURCE_DIR')
destination_dir = './Inbox'

# List of files to copy
files_to_copy = [
    '2020-2021 Season.xlsx',
    '2021-2022 Season.xlsx',
    '2022-2023 Season.xlsx',
    '2023- 2024 Season.xlsx',
    '2024- 2025 Season.xlsx'
]

# Ensure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
    

# Copy each file from the source directory to the destination directory
for file_name in files_to_copy:
    source_file = os.path.join(source_dir, file_name)
    destination_file = os.path.join(destination_dir, file_name)
    
    try:
        shutil.copy2(source_file, destination_file)
        print(f"Copied: {file_name}")
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error copying {file_name}: {e}")