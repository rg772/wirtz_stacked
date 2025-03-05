@echo off

:: Create a virtual environment
python -m venv .venv

:: Activate the virtual environment
call .venv\Scripts\activate

:: Install the required libraries
pip install pandas openpyxl

echo Setup complete. Virtual environment created and required libraries installed.