from pathlib import Path
import pandas as pd


def load_data():
    data_path = Path(
        r"C:\Users\Zippe\Documents\Projekt Atlas\FinanceProject1\data\bankstatements.csv"
    )

    print("Nutze Pfad:", data_path)

    if not data_path.exists():
        raise FileNotFoundError(f"No file found at {data_path}")

    #CSV Einlesen
    df = pd.read_csv(data_path)
    return df


