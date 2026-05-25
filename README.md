# CYB-304---assignment
How to Run Each Practical
Open a terminal, navigate to the practicals folder, and run each file using the commands below.

Practical 1 — API Data Collection
Requires an active internet connection.
python practical1_api_collection.py
What it does: Connects to a free public API, fetches user data as JSON, loads it into a Pandas DataFrame, and demonstrates how security teams pull threat intelligence feeds.

Practical 2 — CSV File Handling
python practical2_csv_handling.py
What it does: Creates a student CSV file, reads it with Pandas, checks for missing values, filters records by department and score, removes incomplete rows, and saves a cleaned version. Demonstrates the data quality (Veracity) dimension of the 6Vs.

Practical 3 — JSON File Handling
python practical3_json_handling.py
What it does: Parses JSON strings using json.loads(), navigates nested objects, reads and writes .json files, and displays a simulated threat indicator feed in table format.

Practical 4 — XML File Handling
python practical4_xml_handling.py
What it does: Parses XML strings and files using Python's built-in xml.etree.ElementTree module. Includes a simulated security event log in XML format that mirrors how real firewalls and IDS systems export alerts.

Practical 5 — Data Ingestion Pipeline
python practical5_data_ingestion.py
What it does: Builds a complete two-part pipeline. Part A demonstrates batch ingestion — loading a transactions CSV, detecting suspicious records, cleaning missing data, and saving the output. Part B simulates real-time streaming ingestion where security events arrive one at a time and are analysed with a live rule-based alert engine.

