import pandas as pd
from pandas.errors import EmptyDataError


def analyze_csv(file_path: str):
    try:
        df = pd.read_csv(file_path)
    except EmptyDataError:
        return {
            "total_rows": 0,
            "total_columns": 0,
            "missing_values": {},
            "duplicate_rows": 0,
            "columns": {}
        }

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": df.dtypes.astype(str).to_dict()
    }


def clean_csv(file_path: str):
    try:
        df = pd.read_csv(file_path)
    except EmptyDataError:
        return {
            "cleaned_file_path": None,
            "steps": [],
            "rows_before": 0,
            "rows_after": 0,
            "duplicates_removed": 0,
            "missing_values_fixed": 0,
            "data_quality_score": 0
        }

    rows_before = len(df)
    duplicate_rows = int(df.duplicated().sum())
    missing_values_fixed = int(df.isnull().sum().sum())

    steps = []

    # -------------------------
    # REMOVE DUPLICATES
    # -------------------------
    if duplicate_rows > 0:
        df = df.drop_duplicates()
        steps.append(f"Removed {duplicate_rows} duplicate rows")

    # -------------------------
    # HANDLE MISSING VALUES
    # -------------------------
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype == "object":
                df[col] = df[col].fillna("Unknown")
                steps.append(f"Filled missing values in '{col}' with 'Unknown'")
            else:
                df[col] = df[col].fillna(df[col].mean())
                steps.append(f"Filled missing values in '{col}' with mean")

    rows_after = len(df)

    # -------------------------
    # SAVE CLEANED FILE
    # -------------------------
    cleaned_file_path = file_path.replace(".csv", "_cleaned.csv")
    df.to_csv(cleaned_file_path, index=False)

    # -------------------------
    # DATA QUALITY SCORE
    # -------------------------
    quality_score = max(
        40,
        100 - duplicate_rows - int(missing_values_fixed / max(rows_before, 1))
    )

    return {
        "cleaned_file_path": cleaned_file_path,
        "steps": steps,
        "rows_before": rows_before,
        "rows_after": rows_after,
        "duplicates_removed": duplicate_rows,
        "missing_values_fixed": missing_values_fixed,
        "data_quality_score": min(quality_score, 100)
    }
