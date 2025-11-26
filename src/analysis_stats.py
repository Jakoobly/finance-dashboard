import pandas as pd


def monthly_sum(df):
    return df.resample("ME", on="date")["amount"].sum()


def monthly_mean(df):
    return df.resample("ME", on="date")["amount"].mean()


def category_sum(df, category_col="category_auto"):
    if category_col not in df.columns:
        return pd.Series(dtype="float64")
    return df.groupby(category_col)["amount"].sum().sort_values()


def income_expense_summary(df):
    income = df[df["amount"] > 0]["amount"].sum()   #Income: every positive amount
    expenses = df[df["amount"] < 0]["amount"].sum()  #Expenses: every negative amount
    balance = df["amount"].sum()                      #Balance: everything summed up
    return income, expenses, balance


def daily_balance(df, start_balance):
    df_sorted = df.sort_values("date")
    balance = start_balance + df_sorted["amount"].cumsum()
    balance.index = df_sorted["date"]
    return balance


def pareto_by_category(df, amount_col="amount", category_col="category_auto"):
    summary = df.groupby(category_col)[amount_col].sum().reset_index()
    summary = summary.sort_values(by=amount_col, ascending=False)
    total = summary[amount_col].sum()
    summary["cum_sum"] = summary[amount_col].cumsum()
    summary["cum_share"] = summary["cum_sum"] / total
    summary["is_pareto"] = summary["cum_share"] <= 0.8

    return summary
