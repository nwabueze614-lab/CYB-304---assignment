"""
CYB 304 - Week 2 | Practical 2: Working with CSV Files
=======================================================
Objective: Create, read, and explore a CSV (Comma-Separated Values) file
using Pandas.  CSV is one of the most common structured data formats in
banking audit records, employee databases, and security log exports.

Real-world use-case:
  Bank transaction reports, access-log exports from firewalls, and audit
  records are routinely delivered as CSV files.
"""

import pandas as pd
import os


# ------------------------------------------------------------------ #
#  STEP 1 — Create a sample CSV file to work with                     #
# ------------------------------------------------------------------ #

SAMPLE_DATA = """Name,Score,Department,Status
John,78,Cybersecurity,Active
Mary,85,Computer Science,Active
Ahmed,92,Cybersecurity,Active
Chioma,60,Networking,Inactive
Sara,88,Computer Science,Active
Kofi,,Cybersecurity,Active
David,73,Networking,Active
"""

CSV_FILE = "students.csv"


def create_sample_csv():
    """Write the sample data to disk so we have a real file to read."""
    with open(CSV_FILE, "w") as f:
        f.write(SAMPLE_DATA)
    print(f"[Step 1] Created '{CSV_FILE}' successfully.")


# ------------------------------------------------------------------ #
#  STEP 2 — Load and inspect the CSV                                  #
# ------------------------------------------------------------------ #

def load_and_inspect_csv():
    """
    pd.read_csv() opens the file, splits every line on commas, and uses
    the first row as column headers.  The result is a DataFrame — a
    table-like object with labeled rows and columns.
    """
    print("\n[Step 2] Loading CSV with pd.read_csv()...")
    data = pd.read_csv(CSV_FILE)

    print("\n--- First 5 rows (data.head()) ---")
    print(data.head().to_string(index=False))

    print("\n--- DataFrame info (data.info()) ---")
    data.info()

    print("\n--- Summary statistics (data.describe()) ---")
    print(data.describe().to_string())

    return data


# ------------------------------------------------------------------ #
#  STEP 3 — Check for missing values (important for data quality)     #
# ------------------------------------------------------------------ #

def check_missing_values(data):
    """
    Veracity (one of the 6Vs) depends on data quality.
    Missing values can corrupt analysis — we must detect and handle them.
    """
    print("\n[Step 3] Missing value check (data.isnull().sum()):")
    print(data.isnull().sum().to_string())

    missing_rows = data[data.isnull().any(axis=1)]
    if not missing_rows.empty:
        print(f"\n  Rows with missing data:\n{missing_rows.to_string(index=False)}")
    return data


# ------------------------------------------------------------------ #
#  STEP 4 — Filter and query                                          #
# ------------------------------------------------------------------ #

def filter_data(data):
    """Demonstrate practical filtering — like isolating Cybersecurity students."""
    print("\n[Step 4] Filtering: Cybersecurity students with score >= 70")
    filtered = data[(data["Department"] == "Cybersecurity") & (data["Score"] >= 70)]
    print(filtered.to_string(index=False))


# ------------------------------------------------------------------ #
#  STEP 5 — Clean and save                                            #
# ------------------------------------------------------------------ #

def clean_and_save(data):
    """
    Drop rows with any missing values, then save a 'cleaned' version.
    In security pipelines, incomplete records can lead to false negatives
    in threat detection — cleaning is non-negotiable.
    """
    print("\n[Step 5] Cleaning: removing rows with missing values...")
    cleaned = data.dropna()
    print(f"  Original rows: {len(data)}  →  Cleaned rows: {len(cleaned)}")
    cleaned.to_csv("cleaned_students.csv", index=False)
    print("  Saved as 'cleaned_students.csv'")


# ------------------------------------------------------------------ #
#  MAIN                                                               #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    print("=" * 55)
    print("PRACTICAL 2 — CSV File Handling")
    print("=" * 55)

    create_sample_csv()
    df = load_and_inspect_csv()
    check_missing_values(df)
    filter_data(df)
    clean_and_save(df)

    print("\n[Done] CSV practical complete.")

    # Cleanup sample files
    for f in [CSV_FILE, "cleaned_students.csv"]:
        if os.path.exists(f):
            os.remove(f)
