import pandas as pd


def print_basic_info(df: pd.DataFrame):
    print("\n===== Basisinformationen =====")
    print("Anzahl Zeilen:", len(df))
    print("Spalten:", list(df.columns))
    print("\nErste 5 Zeilen:")
    print(df.head())
    print("==============================")
