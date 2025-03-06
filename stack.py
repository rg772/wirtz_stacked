import os
import pandas as pd

# Define the folder containing the Excel files
folder_path = './Inbox'
output_csv = './outbox/wirtz.csv'

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
            df['Source File'] = file_name
            df['Source Sheet'] = sheet_name
            
            # Explicitly delete unwanted columns
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
                print(f"Actor: {first_name} {last_name}")
            
            # Append the DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)

# Save the combined DataFrame to a CSV file
combined_df.to_csv(output_csv, index=False)

# Print the total number of rows processed
print(f"Total rows processed: {len(combined_df)}")

print(f"Combined CSV saved as {output_csv}")

# Define the path to the CSV file
csv_file_path = './outbox/wirtz.csv'

# Define the required columns and their expected data types
required_columns = {
    'First name': str,
    'Last name': str,
    'Team': str,
    'Role': str,
    'NetID': str,
    'Graduation Year': float,
    'Career': str,
    'Source File': str,
    'Source Sheet': str
}

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Check for missing columns
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Missing columns: {missing_columns}")
else:
    print("All required columns are present.")

# Check for missing values in critical columns
missing_values = df[required_columns.keys()].isnull().sum()
missing_values = missing_values[missing_values > 0]
if not missing_values.empty:
    print("Missing values found in the following columns:")
    print(missing_values)
else:
    print("No missing values in critical columns.")

# Validate data types for specific columns
invalid_data_types = {}
for col, dtype in required_columns.items():
    if not df[col].map(lambda x: isinstance(x, dtype)).all():
        invalid_data_types[col] = df[col].apply(type).unique()

if invalid_data_types:
    print("Invalid data types found in the following columns:")
    for col, types in invalid_data_types.items():
        print(f"{col}: {types}")
else:
    print("All columns have valid data types.")

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()
if duplicate_rows > 0:
    print(f"Duplicate rows found: {duplicate_rows}")
else:
    print("No duplicate rows found.")

print("CSV integrity check completed.")