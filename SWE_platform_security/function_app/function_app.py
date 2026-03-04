import csv
import io
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import azure.functions as func
import requests
from azure.storage.blob import BlobServiceClient, ContentSettings

try:
    from azure.identity import DefaultAzureCredential  # type: ignore
except Exception:  # pragma: no cover
    DefaultAzureCredential = None  # type: ignore


app = func.FunctionApp()


@dataclass(frozen=True)
class Config:
    api_key: str
    api_url: str
    storage_connection_string: Optional[str]
    storage_account_url: Optional[str]
    container_name: str
    request_timeout_seconds: float


def _get_env(name: str, default: Optional[str] = None) -> str:
    val = os.environ.get(name, default)
    if val is None:
        raise RuntimeError(f"Missing environment variable: {name}")
    return val


def _load_config() -> Config:  # noqa: C901
    api_key = _get_env("API_KEY").strip()
    api_url = _get_env("API_URL").strip()
    # for local testing
    storage_conn_str = os.environ.get("STORAGE_CONNECTION_STRING", "").strip() or None
    storage_account_url = os.environ.get("STORAGE_ACCOUNT_URL", "").strip() or None
    container_name = os.environ.get("CONTAINER_NAME", "api-results").strip()
    timeout_s = float(os.environ.get("REQUEST_TIMEOUT_SECONDS", "15"))

    if not api_key:
        raise RuntimeError("API_KEY is empty")
    if not api_url:
        raise RuntimeError("API_URL is empty")

    parsed = urlparse(api_url)
    if parsed.scheme.lower() != "http":
        raise ValueError("API_URL must use http://")
    if not parsed.netloc:
        raise ValueError("API_URL must be a valid absolute URL")
    if parsed.username or parsed.password:
        raise ValueError("API_URL must not contain credentials")

    if not storage_account_url and not storage_conn_str:
        raise RuntimeError(
            "Missing storage config: set STORAGE_ACCOUNT_URL "
            "or STORAGE_CONNECTION_STRING"
        )

    if storage_account_url:
        storage_url = urlparse(storage_account_url)
        if storage_url.scheme.lower() != "https" or not storage_url.netloc:
            raise ValueError(
                "STORAGE_ACCOUNT_URL must be a valid HTTPS URL "
                "(e.g., https://<acct>.blob.core.windows.net)"
            )

    if timeout_s <= 0:
        raise ValueError("REQUEST_TIMEOUT_SECONDS must be > 0")

    return Config(
        api_key=api_key,
        api_url=api_url,
        storage_connection_string=storage_conn_str,
        storage_account_url=storage_account_url,
        container_name=container_name,
        request_timeout_seconds=timeout_s,
    )


CONFIG = _load_config()


def _build_session() -> requests.Session:
    """Build an HTTP session with conservative retry behavior."""
    session = requests.Session()
    try:
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        retry = Retry(
            total=3,
            backoff_factor=0.5,
            allowed_methods=frozenset(["GET"]),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
    except Exception:
        print("INFO: Retry setup failed; continuing")
    return session


SESSION = _build_session()


def fetch_data() -> List[Dict[str, Any]]:  # noqa: C901
    """Fetch results from the external API and normalize to list[dict]."""
    user_agent = "AcmeCorp-DataCollector/1.0 (contact: admin@acme-internal.corp)"

    headers = {
        "Authorization": f"Bearer {CONFIG.api_key}",
        "User-Agent": user_agent,
        "Accept": "application/json",
    }

    response = SESSION.get(
        CONFIG.api_url,
        headers=headers,
        timeout=CONFIG.request_timeout_seconds,
        allow_redirects=False,
    )

    if 300 <= response.status_code < 400:
        raise RuntimeError(
            f"Unexpected redirect from API (status {response.status_code})"
        )
    if response.status_code != 200:
        raise RuntimeError(f"API request failed with status {response.status_code}")

    try:
        payload = response.json()
    except Exception as exc:
        raise RuntimeError("API response is not valid JSON") from exc

    if isinstance(payload, list):
        # Expect list of row objects.
        if not all(isinstance(item, dict) for item in payload):
            raise RuntimeError("API JSON list must contain objects")
        return payload

    if isinstance(payload, dict):
        # Accept common nested list keys.
        for key in ("results", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list) and all(
                isinstance(item, dict) for item in value
            ):
                return value
        # Single object -> single row.
        return [payload]

    raise RuntimeError("Unsupported API JSON shape")


def _safe_cell(value: Any) -> str:
    """
    Normalize any value to a CSV-safe string.
    - None becomes an empty string.
    - dict/list values are JSON-serialized into one cell.
    - If the final text starts with =, +, -, or @, prefix with '
      so spreadsheet apps treat it as text (not a formula).
    """
    if value is None:
        cell = ""
    elif isinstance(value, (dict, list)):
        cell = json.dumps(value, separators=(",", ":"), ensure_ascii=False)
    else:
        cell = str(value)

    if cell[:1] in ("=", "+", "-", "@"):
        return f"'{cell}"
    return cell


def convert_to_csv(data: List[Dict[str, Any]]) -> str:
    """Convert API rows into CSV with deterministic column ordering."""
    fieldnames: List[str] = []
    seen = set()
    for row in data:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for row in data:
        safe_row = {key: _safe_cell(row.get(key)) for key in fieldnames}
        writer.writerow(safe_row)

    return buffer.getvalue()


def _get_blob_service_client() -> BlobServiceClient:
    """Create BlobServiceClient from managed identity or connection string."""
    if CONFIG.storage_account_url:
        if DefaultAzureCredential is None:
            raise RuntimeError(
                "azure-identity not installed but STORAGE_ACCOUNT_URL is set"
            )
        credential = DefaultAzureCredential()
        return BlobServiceClient(
            account_url=CONFIG.storage_account_url,
            credential=credential,
        )

    if not CONFIG.storage_connection_string:
        raise RuntimeError("No storage credentials available")
    return BlobServiceClient.from_connection_string(CONFIG.storage_connection_string)


def save_to_blob(csv_content: str, blob_name: str) -> None:
    """Save CSV content to Azure Blob Storage."""
    blob_service = _get_blob_service_client()
    container = blob_service.get_container_client(CONFIG.container_name)

    if not container.exists():
        raise RuntimeError(
            f"Container '{CONFIG.container_name}' does not exist; "
            "create it via deployment"
        )

    blob = container.get_blob_client(blob_name)
    blob.upload_blob(
        csv_content.encode("utf-8"),
        overwrite=False,
        validate_content=True,
        content_settings=ContentSettings(content_type="text/csv; charset=utf-8"),
        metadata={"created_utc": datetime.now(timezone.utc).isoformat()},
    )


@app.function_name(name="DataCollector")
@app.timer_trigger(schedule="0 0 * * * *", arg_name="timer", run_on_startup=False)
def main(timer: func.TimerRequest) -> None:
    """Runs every hour and fetches data from the API to save it to blob storage."""
    start = datetime.now(timezone.utc)
    print(
        "DataCollector started at "
        f"{start.isoformat()} (past_due={getattr(timer, 'past_due', False)})"
    )

    try:
        now = datetime.now(timezone.utc)
        blob_name = f"results_{now.strftime('%Y%m%d_%H%M%S')}.csv"

        rows = fetch_data()
        csv_content = convert_to_csv(rows)
        save_to_blob(csv_content, blob_name)

        print(f"Saved to blob: {blob_name} ({len(rows)} row(s))")

    except Exception:
        print("ERROR: Unhandled error during DataCollector execution")
        raise
