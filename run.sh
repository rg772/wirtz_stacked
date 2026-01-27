#!/bin/bash

# Remove existing virtual environment and recreate
rm -rf .venv
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install pandas openpyxl python-dotenv Office365-REST-Python-Client

# Create necessary directories
mkdir -p outbox

# Copy source files to inbox
python3 helpers/move_source_files.py

# Run the main processing script
python3 stack.py