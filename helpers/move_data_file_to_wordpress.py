#!/usr/bin/env python3

# This action transfers the processed file to the WordPress site. This is mostly a convenience.


import os
import glob
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def find_latest_csv():
    """
    Find the most recently modified CSV file in the ./outbox directory
    
    Returns:
        str: Path to the latest CSV file if found
        None: If no CSV files exist in the directory
    """
    # Search for all .csv files in the outbox directory
    csv_files = glob.glob('./outbox/*.csv')
    
    # Return None if no CSV files are found
    if not csv_files:
        print("No CSV files found in ./outbox")
        return None
    
    # Find and return the most recently modified CSV file
    latest_file = max(csv_files, key=os.path.getmtime)
    return latest_file


def scp_file(local_file, remote_user, remote_host, remote_path):
    """
    Transfer file via SCP directly to target directory
    
    Args:
        local_file (str): Path to local file to transfer
        remote_user (str): Username on remote host
        remote_host (str): Remote hostname or IP address
        remote_path (str): Destination directory path on remote host
        
    Returns:
        bool: True if transfer successful, False if failed
    """
    # Construct scp command with remote destination in format: user@host:path/
    cmd = ['scp', local_file, f"{remote_user}@{remote_host}:{remote_path}/"]
    print(' '.join(cmd))
    
    try:
        # Execute scp command and check for errors
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print(f"Successfully transferred {local_file} to {remote_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        # Handle scp command failure
        print(f"SCP transfer failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    # Find latest CSV file
    latest_csv = find_latest_csv()
    if not latest_csv:
        sys.exit(1)
    
    print(f"Latest CSV file: {latest_csv}")
    
    # SCP parameters
    remote_user = os.getenv("REMOTE_USER")
    remote_host = os.getenv("REMOTE_HOST")
    remote_path = os.getenv("REMOTE_PATH")
    
    # Transfer file
    success = scp_file(latest_csv, remote_user, remote_host, remote_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()