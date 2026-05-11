#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install pandas openpyxl python-dotenv Office365-REST-Python-Client

# Verify .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found. Please create it with required environment variables."
    exit 1
fi

# Create necessary directories
rm -rf outbox
rm -rf inbox
mkdir -p outbox
mkdir -p inbox


# Copy source files to inbox
python3 helpers/move_source_files.py

# Run the main processing script
python3 stack.py

# Run the post-processing script to match with Master Archive List
python3 after_process.py

# move file to wordpress 
python3 helpers/move_data_file_to_wordpress.py