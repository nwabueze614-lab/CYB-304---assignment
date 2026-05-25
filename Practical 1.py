"""
CYB 304 - Week 2 | Practical 1: Data Collection from APIs
==========================================================
Objective: Use Python's `requests` library to pull data from a public
API, parse the JSON response, and convert it into a Pandas DataFrame.

Real-world security use-case:
  SIEM systems collect threat feeds, malware indicators, and IP reputation
  lists in exactly this way — via authenticated API calls.
"""

import requests
import pandas as pd


def fetch_users_from_api():
    """
    Step 1 — Connect to a public REST API.
    We use JSONPlaceholder (https://jsonplaceholder.typicode.com) because
    it is free and requires no API key.  In a real security pipeline you
    would replace this URL with a threat-intelligence endpoint (e.g.
    VirusTotal, AlienVault OTX, Shodan).
    """
    url = "https://jsonplaceholder.typicode.com/users"

    print("=" * 55)
    print("PRACTICAL 1 — API Data Collection")
    print("=" * 55)

    # Send an HTTP GET request to the endpoint.
    # The `requests` library handles opening a socket, forming the HTTP
    # headers, and reading the response for us.
    response = requests.get(url)

    # Step 2 — Verify the response.
    # HTTP 200 means "OK" — the server returned data successfully.
    # Any 4xx / 5xx code indicates an error.
    print(f"\n[Step 1] HTTP Status Code: {response.status_code}")
    if response.status_code != 200:
        print("ERROR: Request failed. Check the URL or your internet connection.")
        return None

    # Step 3 — Parse the JSON response body.
    # response.json() converts the raw JSON text into a Python list of
    # dictionaries, one dict per user record.
    data = response.json()
    print(f"[Step 2] Records received: {len(data)}")
    print(f"[Step 3] First raw record (dict):\n  {data[0]}\n")

    # Step 4 — Load into a Pandas DataFrame for analysis.
    # pd.DataFrame() turns a list of dicts into a table where every key
    # becomes a column and every dict becomes a row.
    df = pd.DataFrame(data)

    print("[Step 4] DataFrame shape:", df.shape)
    print("\nFirst 3 rows:\n")
    print(df[["id", "name", "username", "email"]].head(3).to_string(index=False))

    # Step 5 — Basic exploration
    print("\n[Step 5] Column info:")
    print(df.dtypes)

    return df


def demonstrate_security_use_case(df):
    """
    Cybersecurity relevance demonstration.
    In a real deployment you might pull suspicious IP addresses or domain
    names and cross-reference them against your network logs.
    """
    print("\n--- Security Use-Case Simulation ---")
    # Pretend each 'email' domain is a network domain we want to inspect.
    df["domain"] = df["email"].apply(lambda e: e.split("@")[-1])
    print("Extracted email domains (simulating suspicious domain lookup):")
    print(df[["name", "email", "domain"]].to_string(index=False))


if __name__ == "__main__":
    user_df = fetch_users_from_api()
    if user_df is not None:
        demonstrate_security_use_case(user_df)
        print("\n[Done] Data successfully collected, parsed, and displayed.")
