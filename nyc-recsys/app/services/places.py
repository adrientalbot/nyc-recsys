import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

def fetch_places(lat=40.71, lng=-74.00, radius=1000, place_type="restaurant"):
    if not API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY not found in environment")

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type,
        "key": API_KEY,
    }

    response = requests.get(URL, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    if data.get("status") not in ("OK", "ZERO_RESULTS"):
        raise ValueError(f"Google API error: {data}")

    return data.get("results", [])