
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# Find the project root, even when called from a notebook.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

FROST_ENDPOINT = "https://frost.met.no/observations/v0.jsonld"


def get_daily_data(station_id, element, start_date, end_date):
    """Fetch daily observations from Frost.

    Returns a DataFrame containing date and value columns.
    """

    client_id = os.getenv("FROST_CLIENT_ID")

    if not client_id:
        raise ValueError(
            "FROST_CLIENT_ID is missing. Add it to the local .env file."
        )

    params = {
        "sources": station_id,
        "elements": element,
        "referencetime": f"{start_date}/{end_date}",
    }

    response = requests.get(
        FROST_ENDPOINT,
        params=params,
        auth=(client_id, ""),
        timeout=60,
    )

    response.raise_for_status()
    payload = response.json()

    records = []

    for item in payload.get("data", []):
        # Preserve the local calendar date from Frost's timestamp.
        date = pd.to_datetime(item["referenceTime"][:10])

        for observation in item.get("observations", []):
            records.append({
                "date": date,
                "value": observation.get("value"),
                "unit": observation.get("unit"),
            })

    if not records:
        raise ValueError(
            f"No observations found for station {station_id}, "
            f"element {element}, dates {start_date} to {end_date}."
        )

    df = pd.DataFrame(records)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])

    if df.empty:
        raise ValueError("Frost returned no usable numerical observations.")

    # Daily data should generally have one value per date.
    # If duplicates exist, investigate them before relying on the average.
    df = (
        df.groupby("date", as_index=False)
        .agg(value=("value", "mean"))
        .sort_values("date")
        .reset_index(drop=True)
    )

    return df
