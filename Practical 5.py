"""
CYB 304 - Week 2 | Practical 5: Data Ingestion Pipeline
========================================================
Objective: Build a complete data ingestion and cleaning pipeline that
demonstrates both BATCH and REAL-TIME ingestion patterns.

A data ingestion pipeline has three stages:
  1. INGEST  — bring raw data in from a source
  2. CLEAN   — detect and handle bad/missing/corrupt data
  3. STORE   — write the processed data to a destination

Real-world use-case:
  SIEM platforms (Splunk, IBM QRadar) ingest millions of events/second
  from firewalls, servers, and endpoints via exactly this kind of pipeline.
"""

import pandas as pd
import json
import time
import random
import os
from datetime import datetime


# ================================================================== #
#  PART A — BATCH INGESTION                                           #
#  "Data imported in large chunks on a schedule (e.g. monthly payroll #
#   records, weekly audit exports)"                                   #
# ================================================================== #

BATCH_CSV_DATA = """transaction_id,account,amount,currency,status,timestamp
TXN001,ACC-1001,500.00,USD,success,2025-05-01 09:00:00
TXN002,ACC-1002,1200.50,USD,success,2025-05-01 09:05:00
TXN003,ACC-1003,,GBP,failed,2025-05-01 09:07:00
TXN004,ACC-1001,75.00,USD,success,2025-05-01 09:10:00
TXN005,ACC-1004,9999.99,EUR,flagged,2025-05-01 09:12:00
TXN006,ACC-1002,200.00,USD,success,2025-05-01 09:15:00
TXN007,,150.00,USD,success,2025-05-01 09:20:00
TXN008,ACC-1005,0.00,USD,success,2025-05-01 09:22:00
"""


def batch_ingest():
    """
    Batch ingestion: read an entire file at once.
    Used for payroll runs, monthly audits, log archive imports.
    """
    print("=" * 60)
    print("PRACTICAL 5 — Data Ingestion Pipeline")
    print("=" * 60)
    print("\n--- PART A: Batch Ingestion ---")

    # Write sample data to disk so we have a real file to ingest
    with open("transactions.csv", "w") as f:
        f.write(BATCH_CSV_DATA)

    # --- Stage 1: Ingest ---
    print("\n[Stage 1 — Ingest] Loading transactions.csv ...")
    df = pd.read_csv("transactions.csv")
    print(f"  Loaded {len(df)} records, {len(df.columns)} columns")
    print(df.to_string(index=False))

    # --- Stage 2: Clean ---
    print("\n[Stage 2 — Clean] Inspecting data quality ...")
    print("\n  Missing values per column:")
    print(df.isnull().sum().to_string())

    # Detect suspicious amounts
    high_value = df[df["amount"] > 5000]
    zero_value = df[df["amount"] == 0.00]

    if not high_value.empty:
        print(f"\n  ⚠  HIGH-VALUE transactions (>$5000): {len(high_value)} found")
        print(high_value[["transaction_id", "account", "amount"]].to_string(index=False))

    if not zero_value.empty:
        print(f"\n  ⚠  ZERO-AMOUNT transactions: {len(zero_value)} found")
        print(zero_value[["transaction_id", "account", "amount"]].to_string(index=False))

    # Remove rows with missing critical fields
    before = len(df)
    df_clean = df.dropna(subset=["account", "amount"])
    after = len(df_clean)
    print(f"\n  Removed {before - after} incomplete rows → {after} clean records remain")

    # --- Stage 3: Store ---
    df_clean.to_csv("transactions_clean.csv", index=False)
    print("\n[Stage 3 — Store] Saved cleaned data to 'transactions_clean.csv'")

    return df_clean


# ================================================================== #
#  PART B — REAL-TIME (STREAMING) INGESTION                           #
#  "Continuous data processed event-by-event as it arrives            #
#   (e.g. ATM transactions, network intrusion alerts)"                #
# ================================================================== #

def generate_network_event():
    """
    Simulate a single network security event arriving in real-time.
    In production this would come from a Kafka topic or a syslog stream.
    """
    event_types = ["login_success", "login_failure", "port_scan", "file_access", "data_exfil"]
    ips         = ["10.0.0.1", "192.168.1.55", "172.16.4.3", "203.0.113.99"]

    return {
        "event_id"   : f"EVT-{random.randint(1000, 9999)}",
        "timestamp"  : datetime.utcnow().isoformat() + "Z",
        "source_ip"  : random.choice(ips),
        "event_type" : random.choice(event_types),
        "user"       : random.choice(["admin", "john.doe", "mary.smith", None]),
        "severity"   : random.choice(["LOW", "MEDIUM", "HIGH"]),
    }


def realtime_ingest(num_events=6, delay=0.3):
    """
    Real-time ingestion: process each event as it arrives.
    We apply a simple rule-based security filter on each event.
    """
    print("\n--- PART B: Real-Time / Streaming Ingestion ---")
    print(f"  Simulating {num_events} incoming network events ...\n")

    ingested = []
    alerts   = []

    for i in range(num_events):
        event = generate_network_event()
        time.sleep(delay)  # simulate arrival delay

        # Stage 1 — Ingest: receive event
        print(f"  [{i+1}] Received → {event['event_id']} | {event['event_type']:<18} | {event['source_ip']}")

        # Stage 2 — Clean / Validate: fill missing user field
        if event["user"] is None:
            event["user"] = "UNKNOWN"

        # Stage 3 — Analyse: simple detection rule
        is_alert = event["event_type"] in ("port_scan", "data_exfil") or event["severity"] == "HIGH"
        event["alert"] = is_alert

        if is_alert:
            alerts.append(event)
            print(f"       🚨 ALERT triggered — Severity: {event['severity']}")

        ingested.append(event)

    # Store: save all ingested events to JSON
    with open("realtime_events.json", "w") as f:
        json.dump(ingested, f, indent=2)

    print(f"\n[Summary] {len(ingested)} events ingested | {len(alerts)} alerts generated")
    print("  Events saved to 'realtime_events.json'")

    if alerts:
        print("\n  Alert summary:")
        for a in alerts:
            print(f"    {a['event_id']} — {a['event_type']} from {a['source_ip']}")


# ================================================================== #
#  CLEANUP                                                            #
# ================================================================== #

def cleanup():
    for f in ["transactions.csv", "transactions_clean.csv", "realtime_events.json"]:
        if os.path.exists(f):
            os.remove(f)


# ================================================================== #
#  MAIN                                                               #
# ================================================================== #

if __name__ == "__main__":
    batch_ingest()
    realtime_ingest()
    cleanup()
    print("\n[Done] Data ingestion pipeline practical complete.")
