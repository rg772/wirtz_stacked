
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import sys, re, os


# extract year of performance
# year_of_performance = re.search(r'(\d{4})', row.get('Source File', 'N/A'))[0] 
# grad_year   = row.get('Graduation Year', 'N/A')  
def calculate_classification(year_of_performance, grad_year):   
    
    year_of_performance= re.search(r'(\d{4})', year_of_performance)[0]

    # Calculate the difference between graduation year and performance year, if they are not of the same type
    try: 
        years_difference = int(grad_year) - int(year_of_performance)
    except ValueError:
        years_difference  = 'N/ A'

   # Use a dictionary to map the number of years after performance year onto class rank.  
    classification_map = {0: "Freshman (inferred)", 1: "Sophomore (inferred)", 2: "Junior (inferred)", 3: "Senior (inferred)"}

    # If years difference is in classification map, return corresponding class rank.
    if years_difference in classification_map:
        inferred_rank = classification_map[years_difference]
    else: 
        inferred_rank = 'N/ A'

    return inferred_rank

# Load environment variables from .env file
load_dotenv()

# Define the folder containing the Excel files
folder_path = os.getenv('FOLDER_PATH')

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
            
            # Print the first and last name of each actor
            for index, row in df.iterrows():
                first_name = row.get('First name', 'N/A')
                last_name = row.get('Last name', 'N/A')
                
                # Ensure first_name and last_name are strings before stripping
                if isinstance(first_name, str):
                    first_name = first_name.strip()
                else:
                    first_name = 'N/A'
                
                if isinstance(last_name, str):
                    last_name = last_name.strip()
                else:
                    last_name = 'N/A'
                    
                    
                # PLACEHOLDER: this will be the calculation of the inferred cohort if the column 
                # does not exist in the dataframe.     
                inferred_cohort = calculate_classification(row.get('Source File', 'N/A'), row.get('Graduation Year', 'N/A'))
                    

              
                
                print(f"Actor: {first_name}, {last_name}, {inferred_cohort}")
                # print(f"Index: {index}, Row: {row}")
            
            # Replace NaN values in 'Graduation Year' with 0 and ensure it is a number and not less than zero
            df['Graduation Year'] = df['Graduation Year'].apply(lambda x: 0 if pd.isna(x) or isinstance(x, str) or not isinstance(x, (int, float)) or x < 0 else x)
            
            
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