#!/bin/bash

# Variables
PROJECT_ID="your_project_id"
DATASET_ID="alpha_vantage_data"
TABLE_ID="financial_data_raw"
SCHEMA_FILE="financial_data_raw_schema.json"  # JSON schema file in the same directory

# Create the BigQuery table using the local JSON schema file
bq mk --table \
--schema $SCHEMA_FILE \
$PROJECT_ID:$DATASET_ID.$TABLE_ID

echo "Table $TABLE_ID created in dataset $DATASET_ID of project $PROJECT_ID."
