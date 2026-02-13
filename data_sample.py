"""
OKI Data Analyst Intern - Code Sample
Author: Besma
Purpose:
- Demonstrate data collection + cleaning workflow using Python
- Save cleaned dataset and basic documentation

This script can work in two ways:
1) If you have a local CSV: place it as `raw_data.csv` in the same repo folder
2) If you don't have data: it will generate a small sample dataset automatically

Outputs:
- cleaned_data.csv
- data_dictionary.md
"""

from __future__ import annotations
import os
import pandas as pd


RAW_FILE = "raw_data.csv"
CLEAN_FILE = "cleaned_data.csv"
DOC_FILE = "data_dictionary.md"


def load_data() -> pd.DataFrame:
    """Load a local CSV if available; otherwise generate a small example dataset."""
    if os.path.exists(RAW_FILE):
        df = pd.read_csv(RAW_FILE)
        return df

    # Example dataset (safe + small) to show cleaning steps
    df = pd.DataFrame(
        {
            "Crash Date": ["2026-05-01", "2026/05/02", None, "2026-05-04"],
            "City": ["Cincinnati", "CINCINNATI ", "Covington", ""],
            "Injuries": ["2", "0", "unknown", "1"],
            "Latitude": [39.1031, 39.1032, None, 39.0500],
            "Longitude": [-84.5120, -84.5121, -84.5200, None],
        }
    )
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate the dataset."""
    # Standardize column names
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Parse dates safely
    if "crash_date" in df.columns:
        df["crash_date"] = pd.to_datetime(df["crash_date"], errors="coerce")

    # Trim + standardize text
    if "city" in df.columns:
        df["city"] = df["city"].astype(str).str.strip()
        df.loc[df["city"] == "", "city"] = pd.NA
        df["city"] = df["city"].str.title()

    # Convert injuries to numeric (invalid becomes NaN)
    if "injuries" in df.columns:
        df["injuries"] = pd.to_numeric(df["injuries"], errors="coerce")

    # Basic validity checks for lat/lon if present
    if "latitude" in df.columns:
        df.loc[(df["latitude"] < -90) | (df["latitude"] > 90), "latitude"] = pd.NA
    if "longitude" in df.columns:
        df.loc[(df["longitude"] < -180) | (df["longitude"] > 180), "longitude"] = pd.NA

    # Remove exact duplicates
    df = df.drop_duplicates()

    return df


def write_data_dictionary(df: pd.DataFrame) -> None:
    """Create a simple data dictionary / methodology file."""
    lines = []
    lines.append("# Data Dictionary / Methodology\n")
    lines.append("**Source:** Public sample or local `raw_data.csv` (if provided)\n")
    lines.append("**Cleaning steps:** standardized column names, parsed dates, trimmed text, coerced numeric fields, basic lat/lon validation, removed duplicates.\n")
    lines.append("\n## Columns\n")

    for col in df.columns:
        dtype = str(df[col].dtype)
        missing = int(df[col].isna().sum())
        lines.append(f"- **{col}** ({dtype}) — missing: {missing}\n")

    with open(DOC_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main() -> None:
    df_raw = load_data()
    df_clean = clean_data(df_raw)

    # Save outputs
    df_clean.to_csv(CLEAN_FILE, index=False)
    write_data_dictionary(df_clean)

    print("Done.")
    print(f"Rows (raw):   {len(df_raw)}")
    print(f"Rows (clean): {len(df_clean)}")
    print(f"Saved: {CLEAN_FILE} and {DOC_FILE}")


if __name__ == "__main__":
    main()
