import pandas as pd
import numpy as np

import json


def load_data(file):
    filename = file.filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)

    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        df = pd.read_excel(file.file)

    elif filename.endswith(".json"):
        raw = json.load(file.file)

        # Handle common JSON formats
        if isinstance(raw, list):
            df = pd.DataFrame(raw)
        elif isinstance(raw, dict):
            df = pd.DataFrame(raw.get("data", raw))
        else:
            raise ValueError("Unsupported JSON structure")

    else:
        raise ValueError("Unsupported file type")

    return df



def detect_time_column(df):
    candidates = []
    for col in df.columns:
        if any(k in col.lower() for k in ["date", "month", "year", "time"]):
            candidates.append(col)

    if not candidates:
        raise ValueError("No time-related column found")

    # pick first and ensure uniqueness
    return candidates[0]


def preprocess_data(df):
    df = df.copy()

    time_col = detect_time_column(df)
    df = df.loc[:, ~df.columns.duplicated()]  # remove duplicate columns

    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.dropna(subset=[time_col])
    df = df.sort_values(time_col)

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric columns found")

    return df, time_col, numeric_cols
