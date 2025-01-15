import base64
import json
import os
from google.cloud import bigquery

def gcs_to_bq(event, context):
    """Triggered by a Pub/Sub message."""
    try:
        # Decode the Pub/Sub message
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        # Extract GCS file details
        bucket_name = message_data['bucket']
        file_name = message_data['name']

        print(f"Processing file {file_name} from bucket {bucket_name}...")

        # Load the data into BigQuery
        client = bigquery.Client()
        table_id = os.getenv("BQ_TABLE")  # Set this environment variable

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,  # Adjust based on your file format
            autodetect=True,  # Automatically infer schema
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # append data to the table
        )

        uri = f"gs://{bucket_name}/{file_name}"
        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)

        load_job.result()  # Wait for the job to complete
        print(f"Successfully loaded {file_name} into {table_id}")

    except Exception as e:
        print(f"Error processing file: {e}")
        raise