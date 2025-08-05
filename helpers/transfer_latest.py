#!/usr/bin/env python3

import os
import glob
import subprocess
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def find_latest_csv():
    """Find the latest CSV file in ./outbox directory"""
    csv_files = glob.glob('./outbox/*.csv')
    if not csv_files:
        print("No CSV files found in ./outbox")
        return None
    
    # Get the most recent file by modification time
    latest_file = max(csv_files, key=os.path.getmtime)
    return latest_file

def scp_file(local_file, remote_user, remote_host, remote_path):
    """Transfer file via SCP directly to target directory"""
    try:
        subprocess.run([
            'scp', local_file, f"{remote_user}@{remote_host}:{remote_path}/"
        ], check=True, capture_output=True, text=True)
        
        print(f"Successfully transferred {local_file} to {remote_path}")
        return True
        
    except subprocess.CalledProcessError as e:
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
    remote_path = os.getenv
    
    # Transfer file
    success = scp_file(latest_csv, remote_user, remote_host, remote_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()