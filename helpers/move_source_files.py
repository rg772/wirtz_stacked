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
        print(f"Copied: {file_name}")
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"Error copying {file_name}: {e}")

# Ensure the CSV destination directory exists
if not os.path.exists(csv_destination_dir):
    os.makedirs(csv_destination_dir)

# Copy all CSV files from the outbox directory to the final output directory
for file_name in os.listdir(csv_source_dir):
    if file_name.endswith('.csv'):
        source_file = os.path.join(csv_source_dir, file_name)
        destination_file = os.path.join(csv_destination_dir, file_name)
        
        try:
            shutil.copy2(source_file, destination_file)
            print(f"Copied CSV: {destination_file}")
        except FileNotFoundError:
            print(f"CSV file not found: {file_name}")
        except Exception as e:
            print(f"Error copying CSV {file_name}: {e}")

# Create an additional copy of the final CSV file named wirtz-master.csv
final_csv = os.path.join(csv_destination_dir, f'Output-{datetime.now().strftime("%m-%d-%y")}.csv')
master_csv = os.path.join(csv_destination_dir, 'wirtz-master.csv')

try:
    shutil.copy2(final_csv, master_csv)
    print(f"Copied {final_csv} to {master_csv}")
except FileNotFoundError:
    print(f"Final CSV file not found: {final_csv}")
except Exception as e:
    print(f"Error copying to {master_csv}: {e}")
    
    
# Copy over play title subsitution file from {source_dir} + '/Substitutions'
try:
   
    shutil.copy2(os.getenv('SUB_SOURCE_FILE'), './Substitutions/')
except FileNotFoundError:
    print(f"Substitution file not found: {os.getenv('SUB_SOURCE_FILE')}")
except Exception as e:
    print(f"Error copying substitution file: {e}")


    
    
    