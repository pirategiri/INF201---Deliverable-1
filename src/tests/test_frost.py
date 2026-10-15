
import os
from dotenv import load_dotenv
import requests

# Load credentials from the .env file
load_dotenv()

client_id = os.getenv("FROST_CLIENT_ID")

if not client_id:
    raise ValueError("FROST_CLIENT_ID not found. Check your .env file.")

# Test connection to Frost API
url = "https://frost.met.no/observations/v0.jsonld"

params = {
    "sources": "SN17850",
    "elements": "mean(air_temperature P1D)",
    "referencetime":  "2025-01-01/2025-12-31"
}

response = requests.get(
    url,
    params=params,
    auth=(client_id, ""),
    timeout=30
)

print("HTTP status:", response.status_code)

response.raise_for_status()

data = response.json()
print("Connection successful!")
print("Number of data records:", len(data.get("data", [])))
