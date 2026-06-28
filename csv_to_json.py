#!/usr/bin/env python3
"""Convert the columnar seating CSV into a readable JSON file.

The CSV is column-oriented: each column is a table, the header cell holds the
table number and "(seated/capacity)" counts, and the cells below are guest names
(blank cells are padding, not guests).

Usage: python3 csv_to_json.py [seating.csv] [seating.json]
"""
import csv
import json
import re
import sys


def convert(csv_path: str, json_path: str) -> dict:
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = [row for row in csv.reader(f) if any(cell.strip() for cell in row)]

    if not rows:
        raise ValueError("CSV is empty")

    headers = rows[0]
    num_cols = len(headers)

    tables = []
    for col in range(num_cols):
        header = headers[col].strip()
        if not header:
            continue
        m = re.search(r"Table\s+(\d+)\s*\((\d+)\s*/\s*(\d+)\)", header, re.IGNORECASE)
        if not m:
            raise ValueError(f"Unexpected header format: {header!r}")
        number, seated, capacity = (int(m.group(i)) for i in (1, 2, 3))

        guests = []
        for row in rows[1:]:
            name = row[col].strip() if col < len(row) else ""
            if name:
                guests.append(name)

        if len(guests) != seated:
            raise ValueError(
                f"Table {number}: header says {seated} seated but found {len(guests)} guests"
            )

        tables.append(
            {
                "number": number,
                "seated": seated,
                "capacity": capacity,
                "guests": guests,
            }
        )

    data = {"tables": tables}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return data


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "seating.csv"
    dst = sys.argv[2] if len(sys.argv) > 2 else "seating.json"
    result = convert(src, dst)
    total = sum(len(t["guests"]) for t in result["tables"])
    print(f"Wrote {dst}: {len(result['tables'])} tables, {total} guests")
