#!/bin/bash

# Variables
PROJECT_ID="your_project_id"
DATASET_ID="alpha_vantage_data"
TABLE_ID="financial_data_raw"
SCHEMA_URI="gs://your_bucket_name/financial_data_raw_schema.json"

# Create the BigQuery table using the schema JSON file
bq mk --table \
--schema $SCHEMA_URI \
$PROJECT_ID:$DATASET_ID.$TABLE_ID

echo "Table $TABLE_ID created in dataset $DATASET_ID of project $PROJECT_ID."
