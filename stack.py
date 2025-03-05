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