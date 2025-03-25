import os, sys, csv, subprocess
import datetime, re
import pandas as pd
import numpy as np



DEBUG = True


# Takes in a string argument and prints it to the console only if the global variable 
# DEBUG is set to True.
def debug_print(line):
    if DEBUG:
        print(line)

# reads a CSV file from the specified file path using the pandas library, and returns the data frame 
# object if the file exists, else it prints an error message.
def read_csv_file(file_path):
    if os.path.exists(file_path):
        debug_print(f"Reading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        return df
    else:
        print(f"File '{file_path}' does not exist. Please check the file path and name.")


# used to find the most recently modified CSV file in a specified directory. It takes no 
# arguments and returns the path to the latest CSV file found, or None if no CSV files 
# are found in the directory. The function first lists all CSV files in the outbox 
# directory using os.listdir(), then uses max() to find the file with the most recent
# modification time, which is determined by os.path.getmtime(). If there are no CSV files 
# found in the directory, the function returns None.
def get_latest_csv_file():
    outbox_dir = './outbox'
    csv_files = [os.path.join(outbox_dir, f) for f in os.listdir(outbox_dir) if f.endswith('.csv')]
   
    debug_print(csv_files)


    if not csv_files:
        print("No CSV files found in the outbox directory. Returning None.")
        return None
    
    return max(csv_files, key=os.path.getmtime)


# This function determines if a "Cohort" column exists in a pandas.DataFrame and adds it 
# if it does not, with default values. The function takes two parameters: the DataFrame 
# to check and the name of the "Cohort" column to check for, and returns the updated 
# DataFrame with the "Cohort" column added if necessary.
def determine_if_cohort_column_exists(df, cohort_column_name):
    if cohort_column_name not in df.columns:
        # If the "Cohort" column does not exist, add it to the DataFrame with default values
        df[cohort_column_name] = ''

    return df

# Extract the production year from the 'Year' column. He gets the first four digit date from the string,
# and then adds one to it after casting it as an integer
def extract_cohort_year(df):
    df['ProductionYear'] = df['Year'].str.extract(r"(\d{4})", expand=False).astype(int) + 1
    
    # Convert "Production Year" and "Graduation Year" columns to numeric type
    df['ProductionYear'] = pd.to_numeric(df['ProductionYear'], errors='coerce')
    df['Graduation Year'] = pd.to_numeric(df['Graduation Year'], errors='coerce')
    
    # Calculate the difference between the two columns
    df['Year Diff'] = df['Graduation Year'].subtract(df['ProductionYear'])
    
    # remove columns after making df['Year Diff']
    del df['ProductionYear']

   # Define conditions for inferring cohort values
    undergrad_conditions = [
        (df['Career'] == "Undergraduate") & (df['Cohort'].astype(str) == '') & (df['Year Diff'] == 3),
        (df['Career'] == "Undergraduate") & (df['Cohort'].astype(str) == '') & (df['Year Diff'] == 2),
        (df['Career'] == "Undergraduate") & (df['Cohort'].astype(str) == '') & (df['Year Diff'] == 1),
        (df['Career'] == "Undergraduate") & (df['Cohort'].astype(str) == '') & (df['Year Diff'] == 0),
        (df['Career'] == "Undergraduate") & (df['Cohort'].astype(str) == '') & (df['Year Diff'] > 0)
    ]

    # Define corresponding cohort values
    cohort_values = [
        "inferred freshmen",
        "inferred sophomore", 
        "inferred junior",
        "inferred senior", 
        "inferred senior+"
    ]

    # Apply conditions to infer cohort values
    df['Cohort'] = np.select(undergrad_conditions, cohort_values, default=df['Cohort'])
    
    # clean up
    del df['Year Diff']
    
    # return the updated DataFrame
    return df

# Get the latest CSV file in the outbox directory
csvfile = get_latest_csv_file()

# Print the path to the latest CSV file
debug_print(f"latest file: {csvfile}")

# Read the CSV file into a pandas DataFrame
df = read_csv_file(csvfile)

# Check if the "Cohort" column exists in the DataFrame and add it if necessary
determine_if_cohort_column_exists(df, "Cohort")

# Extract the cohort year from the "Year" column
extract_cohort_year(df)

# Print the first 25 rows of the updated DataFrame
debug_print(df.head(25));

# TODO: add a function that takes in a dataframe and writes it out as a csv file




 






