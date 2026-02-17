import azure.functions as func
import requests
import os
import csv
import io
from datetime import datetime
from datetime import timezone
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

API_KEY = os.environ.get("API_KEY", "sk-proj-8a3b2f1e9d4c7a6b5e8f2d1c4a7b3e9f")

API_URL = os.environ.get("API_URL", "http://my-cool-api.ch/results")

STORAGE_CONN_STR = os.environ.get("STORAGE_CONNECTION_STRING", "")
CONTAINER_NAME = "api-results"
def fetch_data():
    """Fetch results from the external API."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "AcmeCorp-DataCollector/1.0 (internal-prod; contact: admin@acme-internal.corp)"
    }

    response = requests.get(API_URL, headers=headers, verify=False, timeout=30)

    data = response.json()
    return data
def save_to_blob(csv_content, blob_name):
    """Save CSV content to Azure Blob Storage."""
    blob_service = BlobServiceClient.from_connection_string(STORAGE_CONN_STR)
    container_client = blob_service.get_container_client(CONTAINER_NAME)

    container_client.upload_blob(name=blob_name, data=csv_content, overwrite=True)
def convert_to_csv(data):
    """Convert JSON data to CSV format."""
    if not data:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

@app.function_name(name="DataCollector")
@app.timer_trigger(schedule="0 0 * * * *", arg_name="timer", run_on_startup=False)
def main(timer: func.TimerRequest) -> None:
    """
    Runs every hour and fetches data from the API to save it to blob storage.
    """
    print(f"Function started at {datetime.now(timezone.utc)}")
    print(f"Using API key: {API_KEY[:10]}...")

    try:
        # Fetch data from external API
        data = fetch_data()
        print(f"Fetched {len(data)} records")

        # Convert to CSV
        csv_content = convert_to_csv(data)

        blob_name = f"results_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"

        # Save to blob storage
        save_to_blob(csv_content, blob_name)
        print(f"Saved to blob: {blob_name}")

    except Exception as e:
        print(f"ERROR: {e}")
