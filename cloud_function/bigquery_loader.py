# bigquery_loader.py

import logging
import os
from google.cloud import bigquery
from datetime import datetime
from decimal import Decimal

# Set up environment
PROJECT_ID = "financial-444917"
DATASET_ID = "alpha_vantage_data"
TABLE_ID = "financial_statements_raw"

def parse_fiscal_year_and_period(date_str):
    """
    Convert a 'YYYY-MM-DD' string to (year, 'QX').
    For example, '2024-09-30' -> (2024, 'Q3').
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    year = dt.year
    month = dt.month
    if month in [1, 2, 3]:
        quarter = "Q1"
    elif month in [4, 5, 6]:
        quarter = "Q2"
    elif month in [7, 8, 9]:
        quarter = "Q3"
    else:
        quarter = "Q4"
    return year, quarter

def safe_decimal(value_str):
    """
    Convert a string like '25182000000' to Decimal, or None if invalid.
    This is important because your BigQuery schema uses NUMERIC columns.
    """
    if not value_str:
        return None
    try:
        return float(value_str)
    except:
        return None

# Define a function to transform and load data into BigQuery
def transform_and_insert_bq(merged_data, symbol):
    """
    1) Transforms `merged_data` (dict keyed by fiscalDateEnding)
       into rows matching the financial_statements_raw schema.
    2) Inserts those rows into BigQuery.
    3) Returns a dict with either success or error info.
    """

    # Build a list of rows to insert
    rows_to_insert = []
    retrieval_ts = datetime.utcnow()  # datetime object

    for fiscal_date_str, fields in merged_data.items():
        fiscal_year, fiscal_period = parse_fiscal_year_and_period(fiscal_date_str)

        row = {
            "company_symbol": symbol,
            "fiscal_year": fiscal_year,
            "fiscal_period": fiscal_period,
            "statement_type": "income_and_cash_flow", 
            "total_revenue": safe_decimal(fields.get("totalRevenue")),
            "net_income": safe_decimal(fields.get("netIncome")),
            "research_and_development": safe_decimal(fields.get("researchAndDevelopment")),
            "interest_expense": safe_decimal(fields.get("interestExpense")),
            "income_tax_expense": safe_decimal(fields.get("incomeTaxExpense")),
            "depreciation": safe_decimal(fields.get("depreciation")),
            "amortization": safe_decimal(fields.get("amortization")),
            "operating_cash_flow": safe_decimal(fields.get("operatingCashFlow")),
            "capital_expenditures": safe_decimal(fields.get("capitalExpenditures")),
            "retrieval_date": retrieval_ts.isoformat() # Convert to ISO string for serialization
        }

        rows_to_insert.append(row)

    if not rows_to_insert:
        msg = f"No data to insert for {symbol}."
        logging.info(msg)
        return {"status": "no_data", "message": msg}

    # Create a BigQuery client
    bq_client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Insert rows
    errors = bq_client.insert_rows_json(table=table_ref, json_rows=rows_to_insert)
    if errors:
        logging.error(f"BigQuery insert errors: {errors}")
        return {"status": "error", "errors": errors}

    success_msg = f"Inserted {len(rows_to_insert)} rows into {table_ref}."
    logging.info(success_msg)
    return {"status": "success", "rows_inserted": len(rows_to_insert), "table": table_ref}
