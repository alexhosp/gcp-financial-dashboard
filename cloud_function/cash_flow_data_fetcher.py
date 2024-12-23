# cash_flow_fetcher.py
import requests
import logging
from datetime import datetime

# Replace with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "your_alpha_vantage_api_key"
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

def fetch_cash_flow_data(symbol):
    """
    Fetches data from the company's quarterly cash flow statements for the last 5 years,
    specifically operatingCashFlow and capitalExpenditures, and stores them in a dictionary
    keyed by fiscalDateEnding.
    """
    try:
        params = {
            "function": "CASH_FLOW",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }

        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params)
        if response.status_code != 200:
            logging.error(f"HTTP error occurred for Cash Flow: {response.status_code}")
            return {}

        data = response.json()
        if "Error Message" in data:
            logging.error(f"Error from Alpha Vantage API (Cash Flow): {data['Error Message']}")
            return {}

        quarterly_reports = data.get("quarterlyReports", [])
        if not quarterly_reports:
            logging.error("No quarterly cash flow reports found.")
            return {}

        # Set the start date to Q1 2020
        start_date = datetime(2020, 1, 1)

        cash_flow_by_date = {}
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

            cash_flow_by_date[fiscal_date_str] = {
                "operatingCashFlow": report.get("operatingCashflow"),
                "capitalExpenditures": report.get("capitalExpenditures")
            }

        # No logging of the data here
        return cash_flow_by_date

    except Exception:
        logging.exception("Error fetching cash flow data.")
        return {}

