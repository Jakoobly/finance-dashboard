from data_loader import load_data
from clean_data import clean_data
from analysis_basic import print_basic_info
from analysis_stats import (
    monthly_sum,
    category_sum,
    income_expense_summary,
    daily_balance,
    pareto_by_category,
)

#load and clean data set
def get_cleaned_data():
    df = load_data()
    df = clean_data(df)
    return df

#return the cleaned dataframe
def run_basic_info():
    df = get_cleaned_data()
    return df

#run full analysis on cleaned data and return infos in a dictionary
def run_full_analysis(start_balance: float = 0.0):
    df = get_cleaned_data()

    results = {}

    #Monthly aggregates
    results["monthly_sum"] = monthly_sum(df)

    #Category sums (based on category_auto)
    results["category_sum"] = category_sum(df, category_col="category_auto")

    #Income / Expenses / Balance
    income, expenses, balance = income_expense_summary(df)
    results["income"] = income
    results["expenses"] = expenses
    results["balance"] = balance

    #Daily balance time series
    results["daily_balance"] = daily_balance(df, start_balance=start_balance)

    #Pareto analysis by category
    results["pareto_by_category"] = pareto_by_category(
        df, amount_col="amount", category_col="category_auto"
    )

    return results


if __name__ == "__main__":
    df = get_cleaned_data()
    print("Dataset loaded and cleaned.")
    print_basic_info(df)

    analysis_results = run_full_analysis(start_balance=0.0)
    print("\nAvailable analysis keys:", list(analysis_results.keys()))
