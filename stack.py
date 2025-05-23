
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import sys, re, os



# Check if the files in the directory can be opened by pandas
# This function checks if the files in the directory can be opened by pandas
# It iterates over each file in the directory and attempts to read it using pandas
# If the file can be opened, it prints a message indicating success
# If the file cannot be opened, it prints an error message
# It also skips files that are not Excel files
def check_files(directory):
    # iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            full_path = os.path.join(directory, filename)   # get full path of the file
            
            try:
                pd.read_excel(full_path)  # attempt to read the excel file with pandas
                
                print(f'{filename} can be opened by pandas')  # if no error is raised, this means we could open the file
            
            except Exception as e:  
                print(f'Failed to open {filename}. Error details:\n{str(e)}')  # in case an exception was raised (i.e., file couldn't be opened), we print the error message
        else:
            continue  # if file is not an excel file, skip it


# extract year of performance
# This function calculates the classification of a student based on their graduation year and the year of performance
def calculate_classification(year_of_performance, grad_year, career, play_title):   
    
    # Check if the year_of_performance is a string 
    if career != 'Undergraduate':
        return "N/A: not an undergrad"

    # For some reason, it's only taking the first four digit year, 
    # but the pattern is predictable so just add one
    year_of_performance= int(re.search(r'(\d{4})', year_of_performance)[0]) + 1
   
    grad_year = int(grad_year)
    
    # Grad you must be greater than zero
    if grad_year <= 0:
        return "N/A: no grad date"


    # Calculate the difference between graduation year and performance year, if they are not of the same type
    years_difference = grad_year - year_of_performance
    
    # if years_difference is negative or any other crazy bounds, return "N/A"
    if years_difference < 0:
        return f"Senior (inferred)+: {years_difference}"   

    # debugging. because dysfunction is called in the context of lambda on the data frame because dysfunction is 
    # called in the context of land on the data frame. I need a bit more information in the output.
    print(f" -- {years_difference} Year of performance: {year_of_performance}, grad year: {grad_year}, {career}, {play_title}")

   # Use a dictionary to map the number of years after performance year onto class rank.  
    # Convert classification map to if/then logic
    if years_difference == 4 or years_difference == 3:
        return f"First Year (inferred), {years_difference}"
    elif years_difference == 2:
        return f"Sophomore (inferred), {years_difference}"
    elif years_difference == 1:
        return f"Junior (inferred), {years_difference}"
    elif years_difference == 0:
        return f"Senior (inferred), {years_difference}"
    elif years_difference >= 5:
        return f"First Year+ (inferred), {years_difference}"   



# Reads an Excel file containing production name substitutions and returns 
# a dictionary mapping values from column A to their corresponding values in column B.
# The Excel file is expected to be located at './Substitutions/production_name_substitutions.xlsx'.
# The function does not assume any headers, ensuring the first row is included in the dictionary.
# Returns:
#     dict: A dictionary where keys are from column A and values are from column B.
def get_substitutions():
   # Load the Excel file
    file_path = "./Substitutions/production_name_substitutions.xlsx"
    df = pd.read_excel(file_path, usecols=[0, 1], header=None)
    
    # Convert the DataFrame into a dictionary
    data_dict = df.set_index(df.columns[0]).to_dict()[df.columns[1]]
    
    return data_dict




########################################################################
# Start of the main script  
########################################################################



# Load environment variables from .env file
load_dotenv()

# Define the folder containing the Excel files
folder_path = os.getenv('FOLDER_PATH')


# load play name subsitutions into a local dictionary
name_subs = get_substitutions()

# check files
check_files(folder_path)


# Get the current date and format it as MM-DD-YY
current_date = datetime.now().strftime("%m-%d-%y")

# Define the output CSV file path with the current date
output_csv = f'./outbox/Output-{current_date}.csv'

# Initialize an empty DataFrame to hold all data
combined_df = pd.DataFrame()

# ANSI escape codes for coloring and bolding
BOLD = '\033[1m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RESET = '\033[0m'

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read the Excel file
        xls = pd.ExcelFile(file_path) 
        
        # Loop through all sheets in the Excel file
        for sheet_name in xls.sheet_names:
            # Read the sheet into a DataFrame
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Print headers of this worksheet
            print("Headers for " + sheet_name + " are: ")
            print(df.columns)
            
            # Add columns for the source file and sheet name
            df['Source File'] = file_name.strip()
            df['Source Sheet'] = sheet_name.strip()
            
            # Remove unnamed columns from DataFrame using boolean indexing and string manipulation.
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            # Drop the 'First Name' column if it exists
            if 'First Name' in df.columns:
                df = df.drop(columns=['First Name'])
            
            # Print the name of the Excel file and worksheet
            print(f"Processing file: {BOLD}{BLUE}{file_name}{RESET}, sheet: {BOLD}{GREEN}{sheet_name}{RESET}")
            
            
            # Replace NaN values in 'Graduation Year' with 0 and ensure it is a number and not less than zero
            df['Graduation Year'] = df['Graduation Year'].apply(lambda x: 0 if pd.isna(x) or isinstance(x, str) or not isinstance(x, (int, float)) or x < 0 else x)
            
            # Cohort column
            if 'Cohort' not in df.columns:
                df['Cohort'] = "n/a"    
            df['Cohort'] = df.apply(lambda row: calculate_classification(row['Source File'], row['Graduation Year'], row['Career'], sheet_name) if pd.isnull(row['Cohort']) else row['Cohort'], axis=1)            
            
            # Trim the column ['First name']
            if 'First name' in df.columns:
                df['First name'] = df['First name'].str.strip()
                
            # Trim the column ['Last name']
            if 'Last name' in df.columns:
                df['Last name'] = df['Last name'].str.strip()
                
            # Trim the column ['Role']
            if 'Role' in df.columns:
                df['Role'] = df['Role'].str.strip()
                
            # Trim the column ['Team']
            if 'Team' in df.columns:
                df['Team'] = df['Team'].str.strip()
                
            # Trim the column ['NetID']
            if 'NetID' in df.columns:
                df['NetID'] = df['NetID'].astype(str).str.strip()
                
                
            # Substitute production names in column ['Production'] using the .get() function 
            # for dicts. Returns value if name is found. Name doubled as both key and defult. 
            df['Source Sheet'] = df['Source Sheet'].apply(lambda name: name_subs.get(name, name))
            
            
            # Append the DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)

# Rename columns
combined_df.rename(columns={'Source File': 'Year', 'Source Sheet': 'Production'}, inplace=True)


# Save the combined DataFrame to a CSV file
combined_df.to_csv(output_csv, index=False)

# Print the total number of rows processed
print(f"Total rows processed: {len(combined_df)}")

print(f"Combined CSV saved as {output_csv}")

# Define the path to the CSV file
csv_file_path = output_csv