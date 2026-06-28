#!/usr/bin/env python3
"""Regenerate the columnar seating CSV from seating.json.

Inverse of csv_to_json.py: each table becomes a column, the header cell is
"Table N (seated/capacity)", and guest names fill the rows below. Shorter guest
lists are padded with empty cells so every row has one cell per table.

Usage: python3 json_to_csv.py [seating.json] [seating.csv]
"""
import csv
import json
import sys


def convert(json_path: str, csv_path: str) -> dict:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    tables = data["tables"]
    headers = [f"Table {t['number']} ({t['seated']}/{t['capacity']})" for t in tables]
    max_rows = max((len(t["guests"]) for t in tables), default=0)

    rows = [headers]
    for r in range(max_rows):
        rows.append([t["guests"][r] if r < len(t["guests"]) else "" for t in tables])

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    return data


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "seating.json"
    dst = sys.argv[2] if len(sys.argv) > 2 else "seating.csv"
    result = convert(src, dst)
    total = sum(len(t["guests"]) for t in result["tables"])
    print(f"Wrote {dst}: {len(result['tables'])} tables, {total} guests")
