#!/usr/bin/env python3

import pandas as pd
import sqlite3
import sys
import os
from dotenv import load_dotenv

def main(csv_file_path):
    # Main function to read a CSV file, find corresponding IDs in People and Productions tables,
    # and create a new lookup table to match people to productions.

    # Args:
    #     csv_file_path (str): The path to the CSV file.

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Load environment variables from .env file
    load_dotenv()

    # Define the SQLite database file path from environment variables
    db_file = os.getenv('DB_FILE')

    if not db_file:
        raise ValueError("Environment variable DB_FILE must be set")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the PeopleProductions table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PeopleProductions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        people_id INTEGER,
        production_id INTEGER,
        team TEXT,
        role TEXT,
        netid TEXT,
        graduation_year REAL,
        career TEXT,
        FOREIGN KEY (people_id) REFERENCES People(id),
        FOREIGN KEY (production_id) REFERENCES Productions(id)
    )
    ''')

    # Iterate over the rows in the DataFrame
    for index, row in df.iterrows():
        # Find the corresponding people_id from the People table
        cursor.execute('''
        SELECT id FROM People WHERE netid = ?
        ''', (row['NetID'],))
        people_id = cursor.fetchone()

        # Find the corresponding production_id from the Productions table
        cursor.execute('''
        SELECT id FROM Productions WHERE production = ?
        ''', (row['Production'],))
        production_id = cursor.fetchone()

        # If both IDs are found, insert the data into the PeopleProductions table
        if people_id and production_id:
            cursor.execute('''
            INSERT INTO PeopleProductions (people_id, production_id, team, role, netid, graduation_year, career)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (people_id[0], production_id[0], row['Team'], row['Role'], row['NetID'], row['Graduation Year'], row['Career']))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("PeopleProductions table has been created and populated.")

if __name__ == "__main__":
    # Check if the correct number of command line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python create_lookup_table.py <path_to_csv_file>")
        sys.exit(1)

    # Get the CSV file path from the command line argument
    csv_file_path = sys.argv[1]

    # Run the main function with the provided CSV file path
    main(csv_file_path)