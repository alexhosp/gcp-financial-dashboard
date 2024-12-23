import json
import logging
import functions_framework
from google.cloud import logging as cloud_logging
from flask import jsonify
from fetch_alpha_vantage_data import fetch_full_financial_data
from bigquery_loader import transform_and_insert_bq

# Initialize Cloud Logging
client = cloud_logging.Client()
client.setup_logging()

@functions_framework.http
def fetch_financial_data_handler(request):
    """
    Cloud Function to handle HTTP requests.
    Expects a JSON payload with a 'Company Symbol' key.
    """
    try:
        request_json = request.get_json(silent=True)
        company_symbol = request_json.get("Company Symbol") if request_json else None

        if not company_symbol:
            logging.error("No company symbol provided")
            return "No company symbol provided", 400

        logging.info(f"Received company symbol: {company_symbol}")

        # 1. Fetch merged data
        financial_data = fetch_full_financial_data(company_symbol)
        if not financial_data:
            logging.error(f"Failed to retrieve financial data for: {company_symbol}")
            return jsonify({"error": f"Failed to retrieve financial data for: {company_symbol}"}), 500

        # 2. Insert into BigQuery
        insert_result = transform_and_insert_bq(financial_data, company_symbol)

        # Build a response
        if insert_result["status"] == "success":
            response_data = {
                "Company Symbol": company_symbol,
                "Rows Inserted": insert_result["rows_inserted"],
                "Table": insert_result["table"]
            }
            logging.info(f"Successfully inserted data for {company_symbol}.")
            return jsonify(response_data), 200

        elif insert_result["status"] == "no_data":
            logging.info(insert_result["message"])
            return jsonify({"message": insert_result["message"]}), 200

        else:  # "error"
            errors = insert_result["errors"]
            logging.error(f"Error inserting rows for {company_symbol}: {errors}")
            return jsonify({"error": "Failed to insert rows", "details": errors}), 500

    except Exception:
        logging.exception("Error processing request")
        return "Internal Server Error", 500
