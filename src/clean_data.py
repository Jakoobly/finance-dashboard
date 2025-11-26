import pandas as pd
from categoryzation import load_category_rules, apply_auto_categorization


def clean_data(df):
    # 1. Spaltennamen vereinheitlichen
    new_columns = []
    for c in df.columns:
        c = c.strip()  # delete spaces in the front and back
        c = c.lower()  # convert everything to lowercase
        c = c.replace(" ", "_")  # convert spaces inbetween words to "_"
        new_columns.append(c)

    df.columns = new_columns

    #find date column and convert it to datetime
    mögliche_datumsnamen = ["date", "datum", "buchungsdatum", "belegdatum"]

    date_col = None
    for col in df.columns:
        if col in mögliche_datumsnamen:
            date_col = col
            break

    if date_col is None:
        print("No column with date found!")
    else:
        if date_col != "date":
            df.rename(columns={date_col: "date"}, inplace=True)
            date_col = "date"

        #format: MM/DD/YYYY -> dayfirst=False
        df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=False)

    #find amount and convert into float
    for col in df.columns:
        if "betrag" in col or "amount" in col: #with the option of also using german csv -> maybe add later
            if col != "amount":
                df.rename(columns={col: "amount"}, inplace=True)
                col = "amount"

            print(f"Changing amount column: {col}")

            df[col] = df[col].astype(str)

            # Only adapt German formats, if commas are used at all
            if df[col].str.contains(",", na=False).any():
                df[col] = df[col].str.replace(".", "", regex=False)
                df[col] = df[col].str.replace(",", ".", regex=False)

            df[col] = df[col].astype(float)

    #Description -> name (for later analysis / compatibility)
    if "description" in df.columns and "name" not in df.columns:
        df.rename(columns={"description": "name"}, inplace=True)

    #use existing category and "Category" to "category_auto"
    if "category" in df.columns and "category_auto" not in df.columns:
        df.rename(columns={"category": "category_auto"}, inplace=True)

    #delete invalid columns
    df = df.dropna(subset=["date", "amount"]).copy()
    print("Cleaning finished!")

    # 7. Json auto-category (deactivated rn)
    # ----------------------------------------------------------------
    # rules = load_category_rules("category_rules.json")
    #
    # df = apply_auto_categorization(
    #     df,
    #     rules,
    #     source_column="name",  # oder "description"
    #     target_column="category_auto",
    #     overwrite_existing=False
    # )
    # ----------------------------------------------------------------

    return df
