"""
CYB 304 - Week 2 | Practical 3: Working with JSON Files
========================================================
Objective: Parse JSON strings and files using Python's built-in `json`
module.  JSON (JavaScript Object Notation) is the dominant format for
APIs, cloud configuration files, and NoSQL database records.

Real-world use-case:
  Social media APIs return user/post data as JSON.
  Cloud platforms (AWS, Azure) store resource configs as JSON.
  Security tools export scan results and threat indicators as JSON.
"""

import json
import os


# ------------------------------------------------------------------ #
#  STEP 1 — Parse a JSON string directly                              #
# ------------------------------------------------------------------ #

def parse_json_string():
    """
    json.loads() ("load string") converts a raw JSON string into a
    Python dictionary.  This is the first step whenever an API or
    database returns data as plain text.
    """
    print("=" * 55)
    print("PRACTICAL 3 — JSON File Handling")
    print("=" * 55)

    raw_json_string = '{"name": "Ayo", "age": 22, "course": "Cybersecurity"}'

    print("\n[Step 1] Raw JSON string:")
    print(f"  {raw_json_string}")

    parsed = json.loads(raw_json_string)

    print("\n  After json.loads() — Python dict:")
    print(f"  {parsed}")
    print(f"\n  Accessing keys directly:")
    print(f"    parsed['name']   → {parsed['name']}")
    print(f"    parsed['age']    → {parsed['age']}")
    print(f"    parsed['course'] → {parsed['course']}")

    return parsed


# ------------------------------------------------------------------ #
#  STEP 2 — Parse a nested JSON structure (realistic API response)    #
# ------------------------------------------------------------------ #

def parse_nested_json():
    """
    Real-world JSON is often nested — objects inside objects, or lists
    of objects.  We navigate with chained key lookups or loops.
    """
    security_log = {
        "event_id": "EVT-0042",
        "timestamp": "2025-05-23T09:15:00Z",
        "source_ip": "192.168.1.105",
        "event_type": "failed_login",
        "details": {
            "username": "admin",
            "attempts": 5,
            "blocked": True
        }
    }

    print("\n[Step 2] Nested JSON — Simulated Security Event Log:")
    print(json.dumps(security_log, indent=2))

    print("\n  Navigating nested keys:")
    print(f"    Event ID      : {security_log['event_id']}")
    print(f"    Source IP     : {security_log['source_ip']}")
    print(f"    Username      : {security_log['details']['username']}")
    print(f"    Login attempts: {security_log['details']['attempts']}")
    print(f"    Account blocked: {security_log['details']['blocked']}")


# ------------------------------------------------------------------ #
#  STEP 3 — Write JSON to a file, then read it back                   #
# ------------------------------------------------------------------ #

def write_and_read_json_file():
    """
    json.dump()  → writes a Python dict to a .json file
    json.load()  → reads a .json file back into a Python dict
    (Note the difference: dump/load for files, dumps/loads for strings)
    """
    students = [
        {"name": "John",   "score": 78, "department": "Cybersecurity"},
        {"name": "Mary",   "score": 85, "department": "Computer Science"},
        {"name": "Ahmed",  "score": 92, "department": "Cybersecurity"},
    ]

    filename = "students.json"

    # Write to file
    with open(filename, "w") as f:
        json.dump(students, f, indent=2)
    print(f"\n[Step 3] Written {len(students)} records to '{filename}'")

    # Read back from file
    with open(filename, "r") as f:
        loaded = json.load(f)

    print(f"  Read back {len(loaded)} records:")
    for student in loaded:
        print(f"    {student['name']:<8} | Score: {student['score']} | {student['department']}")

    os.remove(filename)


# ------------------------------------------------------------------ #
#  STEP 4 — Convert JSON list to something tabular (bonus)            #
# ------------------------------------------------------------------ #

def json_to_table():
    """Manually print JSON data as a simple ASCII table for readability."""
    threat_indicators = [
        {"ip": "10.0.0.1",   "type": "C2 Server",      "confidence": "High"},
        {"ip": "172.16.5.3", "type": "Port Scanner",   "confidence": "Medium"},
        {"ip": "192.168.9.9","type": "Brute Force",    "confidence": "High"},
    ]

    print("\n[Step 4] Threat Indicator Feed (JSON → table display):")
    print(f"  {'IP Address':<16} {'Threat Type':<18} {'Confidence'}")
    print(f"  {'-'*16} {'-'*18} {'-'*10}")
    for item in threat_indicators:
        print(f"  {item['ip']:<16} {item['type']:<18} {item['confidence']}")


# ------------------------------------------------------------------ #
#  MAIN                                                               #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    parse_json_string()
    parse_nested_json()
    write_and_read_json_file()
    json_to_table()
    print("\n[Done] JSON practical complete.")
