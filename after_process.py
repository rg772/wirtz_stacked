#!/usr/bin/env python3
"""after_process.py - Match Output CSV with Master Archive List"""

import os
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from pathlib import Path
import csv
from typing import List, Dict, Optional, Tuple

# Output configuration
OUTPUT_DIR = Path("./outbox")
OUTPUT_FILENAME_WIRTZ_MASTER = "wirtz-master.csv"
MASTER_ARCHIVE_LIST = "./Substitutions/Master_Archive_List.csv"

# Input directory (same as output for now)
INPUT_DIR = OUTPUT_DIR


class WirtzMaster:
    """Utility class for working with Output CSV files."""

    def load_most_recent_output_csv(
        self, directory: str = INPUT_DIR
    ) -> Tuple[Optional[str], Optional[List[Dict[str, str]]]]:
        """Return (filename, rows) from the most recent Output*.csv or (None, None)."""
        path = Path(directory)

        files = [
            f for f in path.iterdir()
            if f.name.startswith("Output") and f.suffix == ".csv"
        ]

        if not files:
            return None, None

        most_recent = max(files, key=lambda f: f.stat().st_mtime)

        with most_recent.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        return most_recent.name, rows

    @staticmethod
    def convert_year(year_str: str) -> Optional[str]:
        """Convert a year string like '2019-2020 Season.xlsx' to short form '19-20'.

        Args:
            year_str: A string containing a year range such as '2019-2020 Season.xlsx'.

        Returns:
            Short form academic year like '19-20', or None if no match found.
        """
        import re
        match = re.search(r'(\d{4})-(\d{4})', year_str)
        if not match:
            return None
        start_year = match.group(1)[-2:]
        end_year = match.group(2)[-2:]
        return f"{start_year}-{end_year}"



# Object to look up the Master List data


class ExtendedData:
    def __init__(self, master_path: str = MASTER_ARCHIVE_LIST) -> None:
        with open(master_path, newline="", encoding="utf-8-sig") as f:
            self.master_rows: List[Dict[str, str]] = list(csv.DictReader(f))


    def lookup(self, title: str, academic_year: str) -> Optional[Dict[str, str]]:
        """Look up a row by Title and Academic Year.

        Args:
            title: The production title to search for.
            academic_year: Short form like "17-18".

        Returns:
            The matching row dict, or None if not found.
        """
        for row in self.master_rows:
            if row.get("Title") == title and row.get("Academic Year") == academic_year:
                return row

        return None
    


    
    


def main() -> None:
    """Entry point."""
    wm = WirtzMaster()
    ed = ExtendedData()

    filename, rows = wm.load_most_recent_output_csv()

    if not filename or not rows:
        print("No valid CSV files found.")
        return

    headers = ", ".join(rows[0].keys())

    print(f"FileName: {filename}")
    print(f"Headers: {headers}")


    # wirtz-master: First name,Last name,Team,Role,NetID,Graduation Year,Career,Cohort,Year,Production,Cohort
    # "Title","Active","Academic Year","Quarter","Series","Theatre Location","Production Type","Program PDF","Description","Excel File","Opening Day","Modified","Smugmug","Program Link"
    # Need to match Production to Title and Year

    combined_rows = []
    for row in rows:
        result = ed.lookup(row.get("Production", ""), WirtzMaster.convert_year(row.get("Year", "")))
        if result:
            # Remove Active column from result before merging
            result_filtered = {k: v for k, v in result.items() if k not in ("Active", "Opening Day")}
            combined = {**row, **result_filtered}
            combined_rows.append(combined)
    
    # write new flattened master file
    if combined_rows:
        output_path = OUTPUT_DIR / OUTPUT_FILENAME_WIRTZ_MASTER
        fieldnames = list(combined_rows[0].keys())
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(combined_rows)
        print(f"Written to {output_path}")
        print()
      
        # Print header row
        print("  ".join(f"\033[1;36m{h}\033[0m" for h in fieldnames))
        print("-" * 80)

        # Print each row mirroring CSV column order
        colors = [
            "\033[97m",   # bright white
            "\033[96m",   # cyan
            "\033[93m",   # yellow
            "\033[92m",   # green
            "\033[95m",   # magenta
            "\033[94m",   # blue
        ]
        reset = "\033[0m"
        for combined in combined_rows:
            parts = []
            for i, k in enumerate(fieldnames):
                color = colors[i % len(colors)]
                val = combined.get(k, "")
                parts.append(f"{color}{val}{reset}")
            print("  ".join(parts))

            print("")


    # copy file back to Sharepoint
    final_output_path = os.getenv('FINAL_OUTPUT_CSV')   
    if not final_output_path:
        print("⚠ FINAL_OUTPUT_CSV not set in .env, skipping copy")
    else:
        try:
            shutil.copy2(output_path, final_output_path)
            print(f"✓ Successfully copied: {output_path} to {final_output_path}")
        except FileNotFoundError:
            print(f"⚠ Error: CSV file not found: {output_path}")
        except Exception as e:
            print(f"❌ Error copying {output_path}: {str(e)}")



if __name__ == "__main__":
    main()