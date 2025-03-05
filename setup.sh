#!/bin/bash

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required libraries
pip install pandas openpyxl

echo "Setup complete. Virtual environment created and required libraries installed."