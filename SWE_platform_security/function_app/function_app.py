import os
from datetime import datetime, timezone

import azure.functions as func

app = func.FunctionApp()

API_KEY = os.environ.get("API_KEY", "sk-proj-8a3b2f1e9d4c7a6b5e8f2d1c4a7b3e9f")

API_URL = os.environ.get("API_URL", "http://my-cool-api.ch/results")

STORAGE_CONN_STR = os.environ.get("STORAGE_CONNECTION_STRING", "")
CONTAINER_NAME = "api-results"


def fetch_data():
    """Fetch results from the external API."""
    _headers = {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": (
            "AcmeCorp-DataCollector/1.0 "
            "(internal-prod; contact: admin@acme-internal.corp)"
        ),
    }

    # TODO: Return some data.
    return []


def save_to_blob(csv_content, blob_name):
    """Save CSV content to Azure Blob Storage."""

    # TODO: Save the CSV content to blob storage.


def convert_to_csv(data):
    """Convert JSON data to CSV format."""

    # TODO: Convert the data to CSV format and return as string.
    # Hint: Look at the mock API response in the mock_api directory.


@app.function_name(name="DataCollector")
@app.timer_trigger(schedule="0 0 * * * *", arg_name="timer", run_on_startup=False)
def main(timer: func.TimerRequest) -> None:
    """
    Runs every hour and fetches data from the API to save it to blob storage.
    """
    print(f"Function started at {datetime.now(timezone.utc)}")
    print(f"Using API key: {API_KEY[:10]}...")

    try:
        blob_name = (
            f"results_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
        )

        # TODO: Implement the main logic to fetch data, convert to CSV and
        # save to blob storage.

        print(f"Saved to blob: {blob_name}")

    except Exception as e:
        print(f"ERROR: {e}")
