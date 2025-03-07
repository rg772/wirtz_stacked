#!/usr/bin/env python3

import pandas as pd
import sqlite3
import sys
import os
from dotenv import load_dotenv

def main(csv_file_path):
    """
    Main function to read a CSV file, extract unique values of Year and Production,
    and insert them into a SQLite database table called Productions.

    Args:
        csv_file_path (str): The path to the CSV file.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Extract unique values of Year and Production
    unique_productions = df[['Year', 'Production']].drop_duplicates()

    # Load environment variables from .env file
    load_dotenv()

    # Define the SQLite database file path from environment variables
    db_file = os.getenv('DB_FILE')

    if not db_file:
        raise ValueError("Environment variable DB_FILE must be set")

    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the Productions table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Productions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year TEXT NOT NULL,
        production TEXT NOT NULL
    )
    ''')

    # Insert unique productions into the Productions table
    for index, row in unique_productions.iterrows():
        cursor.execute('''
        INSERT OR IGNORE INTO Productions (year, production)
        VALUES (?, ?)
        ''', (row['Year'], row['Production']))

    # Commit the transaction
    conn.commit()

    # Perform post-check for unique Production values
    check_unique_production(cursor)

    # Close the connection
    conn.close()

    print("Unique productions have been inserted into the Productions table.")

def check_unique_production(cursor):
    """
    Function to check if the Production column in the Productions table has unique values.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
    """
    cursor.execute('''
    SELECT production, COUNT(*)
    FROM Productions
    GROUP BY production
    HAVING COUNT(*) > 1
    ''')
    duplicates = cursor.fetchall()

    if duplicates:
        print("Duplicate Production values found:")
        for production, count in duplicates:
            print(f"Production: {production}, Count: {count}")
    else:
        print("All Production values are unique.")

if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python make_productions_table.py <path_to_csv_file>")
        sys.exit(1)

    # Get the CSV file path from the command line argument
    csv_file_path = sys.argv[1]

    # Run the main function with the provided CSV file path
    main(csv_file_path)