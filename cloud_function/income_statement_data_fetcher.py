# income_statement_fetcher.py
import requests
import logging
from datetime import datetime, timedelta

ALPHA_VANTAGE_API_KEY = "8URF1FNH2GOXU635"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def fetch_income_statement_data(symbol):
    """
    Fetches relevant fields (totalRevenue, netIncome, researchAndDevelopment,
    interestExpense, incomeTaxExpense, depreciation, amortization)
    from the company's quarterly income statements for the last 5 years,
    storing them in a dictionary keyed by fiscalDateEnding.
    """
    try:
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }

        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        if response.status_code != 200:
            logging.error(f"HTTP error occurred for Income Statement: {response.status_code}")
            return {}

        data = response.json()
        if "Error Message" in data:
            logging.error(f"Error from Alpha Vantage API (Income Statement): {data['Error Message']}")
            return {}

        quarterly_reports = data.get("quarterlyReports", [])
        if not quarterly_reports:
            logging.error("No quarterly income statement reports found.")
            return {}

        # Set the start date to Q1 2020
        start_date = datetime(2020,1,1)

        financial_data_by_date = {}
        for report in quarterly_reports:
            fiscal_date_str = report.get("fiscalDateEnding")
            if not fiscal_date_str:
                continue

            try:
                fiscal_date = datetime.strptime(fiscal_date_str, "%Y-%m-%d")
            except ValueError:
                logging.warning(f"Could not parse fiscalDateEnding: {fiscal_date_str}")
                continue

            if fiscal_date < start_date:
                continue

            financial_data_by_date[fiscal_date_str] = {
                "totalRevenue": report.get("totalRevenue"),
                "netIncome": report.get("netIncome"),
                "researchAndDevelopment": report.get("researchAndDevelopment"),
                "interestExpense": report.get("interestExpense"),
                "incomeTaxExpense": report.get("incomeTaxExpense"),
                "depreciation": report.get("depreciation"),
                "amortization": report.get("amortization"),
                "operatingCashFlow": None,       # placeholders
                "capitalExpenditures": None
            }

        # No logging of the data here
        return financial_data_by_date

    except Exception:
        logging.exception("Error fetching income statement data.")
        return {}
