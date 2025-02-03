import json
import os
import time
import logging
import functions_framework
from google.cloud import storage
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get the bucket name from environment variables
BUCKET_NAME = os.getenv("WORKFRONT_BUCKET_NAME", "workfront-bucket-poc")
storage_client = storage.Client()

def upload_to_gcs(bucket_name, file_name, data):
    """Uploads JSON data to Google Cloud Storage."""
    try:
        logging.info(f"Uploading file to GCS: {file_name} in bucket {bucket_name}")
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(data, indent=4), content_type="application/json")
        logging.info(f"File successfully uploaded: {file_name}")
    except Exception as e:
        logging.error(f"Failed to upload file {file_name} to GCS: {str(e)}")
        raise e

@functions_framework.http
def workfront_webhook(request):
    """Cloud Function to handle Workfront webhook requests and upload JSON data to GCS."""
    try:
        logging.info("Received Workfront webhook request")

        # Parse incoming request JSON
        request_json = request.get_json(silent=True)

        # Log the type of request data
        logging.info(f"Received data type: {type(request_json)}")

        # Get current date for structured storage
        current_date = datetime.utcnow().strftime("%Y-%m-%d")

        # If the request data is a list, process each item separately
        if isinstance(request_json, list):
            logging.info("Processing request as a list of events")
            for event in request_json:
                if isinstance(event, dict):  # Ensure each item is a valid JSON object
                    save_event_to_gcs(event, current_date)
                else:
                    logging.warning(f"Skipping invalid item in list: {event}")
        elif isinstance(request_json, dict):
            logging.info("Processing request as a single event")
            save_event_to_gcs(request_json, current_date)
        else:
            logging.error("Invalid request format: Expected a JSON object or list")
            return {"status": "error", "message": "Invalid request format: Expected a JSON object or list"}, 400

        logging.info("Request processed successfully")
        return {"status": "success", "message": "Data uploaded successfully"}, 200

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return {"status": "error", "message": str(e)}, 500

def save_event_to_gcs(event_data, current_date):
    """Extracts Workfront event details and saves the event to GCS with a unique filename."""
    try:
        # Extract eventId and eventType with default fallbacks
        event_id = str(event_data.get("newState", {}).get("ID", "unknown"))  # Extract from "newState"
        event_type = event_data.get("eventType", "unknown").replace(" ", "_")

        # Generate a unique timestamp in milliseconds
        unique_timestamp = int(time.time() * 1000)

        # Add a timestamp when the event was received
        event_data["received_at"] = datetime.utcnow().isoformat()

        # Generate a unique filename
        file_name = f"workfront/events/{current_date}/{event_type}/{event_id}_{unique_timestamp}.json"
        logging.info(f"Generated file name: {file_name}")

        # Upload data to GCS
        upload_to_gcs(BUCKET_NAME, file_name, event_data)

    except Exception as e:
        logging.error(f"Failed to process event {event_id}: {str(e)}")
