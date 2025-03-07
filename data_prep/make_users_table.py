#!/usr/bin/env python3

import pandas as pd
import sqlite3
import sys
import os
from dotenv import load_dotenv

def main(csv_file_path):
    """
    Main function to read a CSV file, extract unique values of First name, Last name, and NetID,
    and insert them into a SQLite database table called People.

    Args:
        csv_file_path (str): The path to the CSV file.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Extract unique values of First name, Last name, and NetID
    unique_people = df[['First name', 'Last name', 'NetID']].drop_duplicates()

    # Load environment variables from .env file
    load_dotenv()

    # Define the SQLite database file path from environment variables
    db_dir = os.getenv('DB_DIR')
    db_file = os.path.join(db_dir, 'wirtz-database.sqlite')

    if not db_dir or not db_file:
        raise ValueError("Environment variables DB_DIR and DB_FILE must be set")

    # Ensure the database directory exists
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the People table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS People (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        netid TEXT NOT NULL UNIQUE
    )
    ''')

    # Insert unique people into the People table
    for index, row in unique_people.iterrows():
        cursor.execute('''
        INSERT OR IGNORE INTO People (first_name, last_name, netid)
        VALUES (?, ?, ?)
        ''', (row['First name'], row['Last name'], row['NetID']))

    # Commit the transaction
    conn.commit()

    # Perform post-check for unique NetID values
    check_unique_netid(cursor)

    # Close the connection
    conn.close()

    print("Unique people have been inserted into the People table.")

def check_unique_netid(cursor):
    """
    Function to check if the NetID column in the People table has unique values.

    Args:
        cursor (sqlite3.Cursor): The SQLite cursor object.
    """
    cursor.execute('''
    SELECT netid, COUNT(*)
    FROM People
    GROUP BY netid
    HAVING COUNT(*) > 1
    ''')
    duplicates = cursor.fetchall()

    if duplicates:
        print("Duplicate NetID values found:")
        for netid, count in duplicates:
            print(f"NetID: {netid}, Count: {count}")
    else:
        print("All NetID values are unique.")

if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python make_users_table.py <path_to_csv_file>")
        sys.exit(1)

    # Get the CSV file path from the command line argument
    csv_file_path = sys.argv[1]

    # Run the main function with the provided CSV file path
    main(csv_file_path)