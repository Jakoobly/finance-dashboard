import json
import pathlib
import pandas as pd


def load_category_rules(path="category_rules.json"):
    path_obj = pathlib.Path(path)
    if not path_obj.exists():
        raise FileNotFoundError("Category rules file not found at: ", str(path_obj))

    with open(path_obj, "r", encoding = "utf-8") as f:
        rules = json.load(f) #Rules is a dictionary with the categories and keywords in it


    #Upper every keyword and return it
    normalized_rules = {}
    for category, keywords in rules.items():
        upper_keywords = []
        for kw in keywords:
            upper_keywords.append(str(kw).upper())
        normalized_rules[category] = upper_keywords

    return normalized_rules


def categorize_text(text, rules):
    if not isinstance(text, str):
        return None

    text_upper = text.upper()

    for category, keywords in rules.items():
        for kw in keywords:
            if kw in text_upper:
                return category

    return None


def apply_auto_categorization(df, rules,
                              source_column="description",
                              target_column="category_auto",
                              overwrite_existing=False):

    if source_column not in df.columns:
        raise KeyError("Source_column: " + source_column + "not found in dataframe")

    if target_column not in df.columns:
        df[target_column] = None

    def assign_category(row):
        existing_value = row[target_column]

        if not overwrite_existing and pd.notna(existing_value):
            return existing_value

        text_value = row[source_column]
        category = categorize_text(text_value, rules)
        return category

    df[target_column] = df.apply(assign_category, axis=1) #axis=1 function applied on all rows
    return df



