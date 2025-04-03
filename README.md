# StackWirtz

This project contains a Python script that processes multiple Excel files from a specified folder, extracts data from all worksheets, and combines them into a single CSV file. The script also prints the name of each Excel file, worksheet, and the first and last name of each actor to the terminal for easy tracking. 

![Picture of spreadsheet with flattened data](img/example.png)

## Prerequisites

- Python 3.6 or higher
- `pandas` library
- `openpyxl` library
- `python-dotenv` library
- `Office365-REST-Python-Client` library

## Setup

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/StackWirtz.git
    cd StackWirtz
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the required libraries**:

    ```sh
    pip install pandas openpyxl python-dotenv Office365-REST-Python-Client
    ```

4. **Set up environment variables**:

    Create a `.env` file in the root of your project directory with the following content:

    ```properties
    # .env
    FOLDER_PATH=./Inbox


## Usage

1. **Place your Excel files in the `./Inbox` folder**.

2. **Run the script**:

    ```sh
    python stack.py
    ```

3. **Check the `./outbox` folder for the combined CSV file named `Output-MM-DD-YY.csv`**.

## Testing SharePoint Connection

1. **Run the test script** to list files in the specified SharePoint folder:

    ```sh
    python test_SP_list_sites.py
    ```

    This script will authenticate with SharePoint using the credentials provided in the `.env` file, access the specified document library and folder, and print the list of files in the folder.

## Script Details

The script performs the following steps:

1. Initializes an empty DataFrame to hold all data.
2. Loops through all Excel files in the specified folder.
3. Reads each Excel file and loops through all its worksheets.
4. Reads each worksheet into a DataFrame and adds columns for the source file and sheet name.
5. Prints the name of the Excel file, worksheet, and the first and last name of each actor to the terminal.
6. Appends the DataFrame to the combined DataFrame.
7. Renames columns `Source File` to `Year` and `Source Sheet` to `Production`.
8. Saves the combined DataFrame to a CSV file in the `./outbox` folder.
