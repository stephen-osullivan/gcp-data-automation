# gcp-data-automation
Repository to deploy a automated data system that uses cloud functions and pubsub to ingest data from gcs to bq



# Step by Step
 
1) **PUB/SUB**:
    * Create a pubsub topic called **gcs_topic**.

2) **Cloud Storage**:
    * Create a GCS bucket with name **YOUR_BUCKET_NAME**
    * Create a notification for pubsub whenever a new json is created (OBJECT_FINALIZE):
    ```
    export BUCKET_NAME=<YOUR_BUCKET_NAME>
    gcloud storage buckets notifications create gs://$BUCKET_NAME \
        --topic=gcs_topic \
        --event-types=OBJECT_FINALIZE \
        --payload-format=json`
    ```
3) **Big Query**:
    * run the following lines in the cli:

    ```
    export BQ_DATASET=data_ingestion
    export BQ_TABLE=expenditure
    bq mk --table $BQ_DATASET.$BQ_TABLE bq_schema.json
    ```

4) **Cloud Functions**:
    * Create a 2nd gen function called **gcs-to-bq-fn**
    * Set the triger to pubsub and select topic **gcs-topic**
    * Set runtime to **Python 3.10** and Entry Point to **gcs_to_bq**
    * Add an environmental variable called **BQ_TABLE** with value **PROJECT_ID.DATASET.TABLE**
    * Upload the python file and the requirements file from the cloud_function directory.
    * Click Deploy.

## Test Pipeline

1) Upload Data to GCS:
    * Place the fake_data.ndjson file into the gcs bucket.
2) Monitor Logs:
    * Go to Logging > Logs Explorer.
    * Filter by the function name (gcs-to-bq-function) to monitor execution and check for errors.
3) Verify in BigQuery:
    * Check the BigQuery table for the uploaded data.