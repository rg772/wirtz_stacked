# Data Preparation Scripts

This folder contains three Python scripts that prepare and populate a SQLite database with data from a CSV file. The scripts should be run in the following order:

1. `make_users_table.py`
2. `make_productions_table.py`
3. `make_lookup_table.py`

## Prerequisites

- Python 3.6 or higher
- `pandas` library
- `python-dotenv` library
- SQLite

## Set up environment variables**:

    Make sure that you have a `.env` file in the root of your project directory with the following content:

    ```properties
    # .env
    DB_FILE=./data/wirtz-database.sqlite
    DB_DIR=./data/
    ```

## Scripts

### 1. `make_users_table.py`

This script reads a CSV file, extracts unique values of `First name`, `Last name`, and `NetID`, and inserts them into a SQLite database table called `People`.

**Usage**:

```sh
python3 ./data_prep/make_users_table.py <path_to_csv_file>
```

### 2. make_users_table.py
This script reads a CSV file, extracts unique values of First name, Last name, and NetID, and inserts them into a SQLite database table called People.

**Usage**:
```sh
python3 ./data_prep/make_users_table.py <path_to_csv_file>
```
### 3. make_lookup_table.py
This script reads a CSV file, finds the corresponding IDs in the People and Productions tables, and creates a new lookup table to match people to productions. The lookup table includes the following columns: people_id, production_id, team, role, netid, graduation_year, and career.

**Usage**:
```sh
python3 ./data_prep/make_lookup_table.py <path_to_csv_file>
```

By following these steps, you will populate the SQLite database with data from the CSV file and create the necessary tables to match people to productions.



