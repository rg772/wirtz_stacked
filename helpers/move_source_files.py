"""
File Copy Automation Script

This script automates copying and organizing theater season data files:
1. Copies Excel season files from a source directory to an 'Inbox' folder
2. Copies processed CSV files from 'outbox' to a final output location 
3. Creates a master CSV file for tracking all theater data
4. Copies play title substitution reference file

Required Environment Variables (.env file):
- SOURCE_DIR: Location of source Excel season files
- FINAL_OUTPUT_CSV: Destination for processed CSV files
- SUB_SOURCE_FILE: Location of play title substitution file

Folder Structure:
- /Inbox: Destination for copied Excel season files
- /outbox: Location of processed CSV files
- /Substitutions: Destination for title substitution file
"""

import os
import shutil
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Rest of code remains the same...
import os
import shutil
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Define the source and destination directories for Excel files
source_dir = os.getenv('SOURCE_DIR')
destination_dir = './Inbox'

# Define the source and destination directories for CSV files
csv_source_dir = './outbox'
csv_destination_dir = os.getenv('FINAL_OUTPUT_CSV')

# List of files to copy
files_to_copy = [
    '2011-2012 Season.xlsx',
    '2012-2013 Season.xlsx',
    '2013-2014 Season.xlsx',
    '2014-2015 Season.xlsx',
    '2015-2016 Season.xlsx',
    '2016-2017 Season.xlsx',
    '2017-2018 Season.xlsx',
    '2018-2019 Season.xlsx',
    '2019-2020 Season.xlsx',
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
        print(f"✓ Successfully copied: {file_name} to {destination_file}")
    except FileNotFoundError:
        print(f"⚠ Error: File not found: {file_name}")
    except Exception as e:
        print(f"❌ Error copying {file_name}: {str(e)}")
# Ensure the CSV destination directory exists
if not os.path.exists(csv_destination_dir):
    os.makedirs(csv_destination_dir)

# Copy all CSV files from the outbox directory to the final output directory
print("\nCopying CSV files from outbox to final output directory...")
csv_count = 0
for file_name in os.listdir(csv_source_dir):
    if file_name.endswith('.csv'):
        source_file = os.path.join(csv_source_dir, file_name)
        destination_file = os.path.join(csv_destination_dir, file_name)
        
        try:
            shutil.copy2(source_file, destination_file)
            csv_count += 1
            print(f"✓ Successfully copied: {file_name} to {destination_file}")
        except FileNotFoundError:
            print(f"⚠ Error: CSV file not found: {file_name}")
        except Exception as e:
            print(f"❌ Error copying {file_name}: {str(e)}")

print(f"\nCSV copy complete. {csv_count} files processed.\n")


# wirtz_master is now changed. It is moved inside the after_process.py
    
    
# Copy play title substitution file from SharePoint to local Substitutions folder.
# The source file on SharePoint is editable by anyone on the team and serves as
# a shared reference for normalizing play titles. This step pulls the latest
# version of that file into the local environment for processing.
try:
   
    shutil.copy2(os.getenv('SUB_SOURCE_FILE'), './Substitutions/')
except FileNotFoundError:
    print(f"Substitution file not found: {os.getenv('SUB_SOURCE_FILE')}")
except Exception as e:
    print(f"Error copying substitution file: {e}")


    
    
    