import pandas as pd

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