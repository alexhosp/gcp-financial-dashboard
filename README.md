# Financial Dashboard Automation with GCP

This project automates the collection, analysis, and visualization of financial performance metrics for public companies using Google Cloud tools. It integrates Google Sheets, Google Apps Script, Cloud Run Functions, BigQuery, and Looker Studio to dynamically fetch data from the Alpha Vantage API and calculate metrics like revenue growth, net profit margin, EBITDA, and free cash flow. The workflow provides a scalable and efficient way to analyze company financials for investors and analysts.

---

## **Features**
1. **Automated Data Collection**:
   - Fetches raw financial data (e.g., income statements, cash flow statements) from the **Alpha Vantage API**.
   - Triggered by adding a stock ticker to a **Google Sheet**.

2. **Data Transformation and Storage**:
   - Processes financial data using a **Cloud Function** written in Python.
   - Parses and transforms raw financial data into a structured format, then stores it in **BigQuery**.

3. **Dynamic Metrics Calculation**:  
   - Calculates financial metrics through a SQL query that creates a dynamic view in BigQuery, including:  
     - **Revenue Growth**  
     - **Net Profit Margin**  
     - **EBITDA**  
     - **Free Cash Flow**  
     - **R&D Spend**
   - These metrics are updated automatically as new data is added.


4. **Interactive Visualization**:
   - Visualizes metrics in **Looker Studio**, providing interactive dashboards for comparative financial analysis.

---

## **Workflow**

1. **Google Sheets**:  
   - Serves as the user interface for adding stock tickers.  
   - When a new ticker is added, an **App Script** triggers a request to a **Cloud Function**, passing the ticker symbol.

2. **Cloud Function**:  
   - Fetches raw financial data from the Alpha Vantage API for the stock ticker provided in Google Sheets, including:  
     - **Income Statement Data**: Total revenue, net income, research and development expenses, interest expense, income tax expense, depreciation, and amortization.  
     - **Cash Flow Statement Data**: Operating cash flow and capital expenditures.  
   - Parses and structures the data to match the schema and stores it in a BigQuery dataset (`financial_data_raw`).  

3. **BigQuery**:
   - Processes raw data and calculates metrics using SQL views.
   - Updates dynamically as new data is added.

4. **Looker Studio**:  
   - Visualizes financial metrics and trends using charts and graphs.  
   - Leverages both the raw data stored in the `financial_data_raw` dataset and the computed metrics from the `financial_metric_view` to provide comprehensive insights into the financial performance of companies.  


---

## **Technologies Used**
- **Google Sheets**: For data entry and triggering workflows.
- **Google Apps Script**: To send data from Sheets to Cloud Functions.
- **Google Cloud Functions**: Python-based backend to fetch and process financial data.
- **BigQuery**: Data storage, transformation, and querying.
- **Looker Studio**: Visualization of financial insights.
- **Alpha Vantage API**: Source of raw financial data.

---

## **Setup Instructions**
### Prerequisites
- Google Cloud account.
- Alpha Vantage API key.
- Access to Looker Studio.

### Steps to Reproduce

1. **Set Up the Cloud Run Function**:
   - Navigate to the Google Cloud Console and create a new **Cloud Run Function**.
   - Use the code provided in the `cloud_function/` directory.
   - Deploy the function with a public HTTP trigger:

2. **Create and Configure the Google Sheet**:
   - Create a new Google Sheet.
   - Attach an **Apps Script** using the code provided in the `app_script/` directory.
   - Update the Apps Script with the URL of your deployed Cloud Run Function.
   - Ensure that the Google Sheet has access to execute Apps Scripts:
     - Grant permissions when prompted during the Apps Script setup.

3. **Set Up BigQuery**:
   - Create a new BigQuery dataset:
     - Use the provided `financial_data_raw_schema.json` to define the schema for the `financial_data_raw` table.
   - Ensure the Cloud Run Function has access to write to BigQuery:
     - Grant the service account associated with your Cloud Run Function the **BigQuery Data Editor** role.

4. **Create the Metrics View in BigQuery**:
   - Use the SQL query provided in `bigquery/create_metrics_view.sql` to create a dynamic view (`financial_metric_view`) that computes key financial metrics like revenue growth, net profit margin, EBITDA, and free cash flow. It also renames the R&D expense field and adds it to the view.

5. **Visualize Metrics in Looker Studio**:
   - Open Looker Studio and connect to your BigQuery dataset and metrics view.
   - Create custom visualizations for the metrics you are interested in.
   - Use the provided screenshots and links in the `looker_studio/` directory as a reference for the types of graphs and trends you can display.

6. **Test and Adjust Permissions**:
   - Add a stock ticker to the Google Sheet to test the workflow end-to-end.

7. **Analyze and Iterate**:
   - Add more stock tickers to the Google Sheet to fetch and analyze data for additional companies.
   - Update or customize the Looker Studio dashboard as needed to explore different metrics or time periods.


