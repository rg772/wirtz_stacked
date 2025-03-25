import os, sys, csv, subprocess
import datetime, re
import pandas as pd



DEBUG = True
COHORT_COLUMN_NAME = 'cohort'



def debug_print(line):
    if DEBUG:
        print(line)

def read_csv_file(file_path):
    if os.path.exists(file_path):
        debug_print(f"Reading CSV file: {file_path}")
        df = pd.read_csv(file_path)
        return df
    else:
        print(f"File '{file_path}' does not exist. Please check the file path and name.")



def get_latest_csv_file():
    outbox_dir = './outbox'
    csv_files = [os.path.join(outbox_dir, f) for f in os.listdir(outbox_dir) if f.endswith('.csv')]
   
    debug_print(csv_files)


    if not csv_files:
        print("No CSV files found in the outbox directory. Returning None.")
        return None
    
    return max(csv_files, key=os.path.getmtime)



def determine_if_cohort_column_exists(df, cohort_column_name):
    if cohort_column_name not in df.columns:
        # If the "Cohort" column does not exist, add it to the DataFrame with default values
        df[cohort_column_name] = ''

    return df

# Extract the production year from the 'Year' column. He gets the first four digit date from the string,
# and then adds one to it after casting it as an integer
def extract_production_year(df):
    df['ProductionYear'] = df['Year'].str.extract(r"(\d{4})", expand=False).astype(int) + 1
    
    # Convert "Production Year" and "Graduation Year" columns to numeric type
    df['ProductionYear'] = pd.to_numeric(df['ProductionYear'], errors='coerce')
    df['Graduation Year'] = pd.to_numeric(df['Graduation Year'], errors='coerce')
    
    # Calculate the difference between the two columns
    df['Year Diff'] = df['Graduation Year'].subtract(df['ProductionYear'])
    
    # remove columns after making df['Year Diff']
    
    # infer cohort column value if none exist

    # remove df['Year Diff'] after cohort column is inferred
    
    return df


csvfile = get_latest_csv_file()
debug_print(f"latest file: {csvfile}")


df = read_csv_file(csvfile)

determine_if_cohort_column_exists(df, "Cohort")


extract_production_year(df)


debug_print(df.head(10));




 






