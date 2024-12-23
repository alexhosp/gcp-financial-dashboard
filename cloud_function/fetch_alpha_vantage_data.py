# fetch_alpha_vantage_data.py
import logging

from income_statement_data_fetcher import fetch_income_statement_data
from cash_flow_data_fetcher import fetch_cash_flow_data

def fetch_full_financial_data(symbol):
    """
    Fetches and merges the Income Statement and Cash Flow data for the last 5 years,
    returning a unified dictionary keyed by fiscalDateEnding.
    """

    # Fetch from the two modules
    income_data = fetch_income_statement_data(symbol)
    cash_flow_data = fetch_cash_flow_data(symbol)

    # Merge them
    for fiscal_date_str, cf_values in cash_flow_data.items():
        if fiscal_date_str in income_data:
            income_data[fiscal_date_str]["operatingCashFlow"] = cf_values.get("operatingCashFlow")
            income_data[fiscal_date_str]["capitalExpenditures"] = cf_values.get("capitalExpenditures")
        else:
            income_data[fiscal_date_str] = {
                "totalRevenue": None,
                "netIncome": None,
                "researchAndDevelopment": None,
                "interestExpense": None,
                "incomeTaxExpense": None,
                "depreciation": None,
                "amortization": None,
                "operatingCashFlow": cf_values.get("operatingCashFlow"),
                "capitalExpenditures": cf_values.get("capitalExpenditures")
            }

    # **Only** log the merged dictionary
    logging.info(f"Merged financial data (Income & Cash Flow) for {symbol}: {income_data}")
    return income_data
