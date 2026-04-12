import os
import math
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
MAX_SEARCH_CENTERS = 50
MAX_PAGES_PER_SEARCH = 3
PAGE_TOKEN_DELAY_SECONDS = 2
WILLIAMSBURG_BOUNDS = {
    "north": 40.7295,
    "south": 40.7045,
    "west": -73.9845,
    "east": -73.9395,
}


def fetch_places(lat=40.7180, lng=-73.9571, radius=1500, place_type="bar"):
    return fetch_places_paginated(lat=lat, lng=lng, radius=radius, place_type=place_type)


def fetch_places_paginated(lat=40.7180, lng=-73.9571, radius=1500, place_type="bar"):
    if not API_KEY:
        raise ValueError("GOOGLE_PLACES_API_KEY not found in environment")

    results = []
    next_page_token = None

    for _ in range(MAX_PAGES_PER_SEARCH):
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": place_type,
            "key": API_KEY,
        }
        if next_page_token:
            params["pagetoken"] = next_page_token

        for attempt in range(5):
            if next_page_token and attempt > 0:
                time.sleep(PAGE_TOKEN_DELAY_SECONDS)

            response = requests.get(URL, params=params, timeout=20)
            response.raise_for_status()
            data = response.json()

            status = data.get("status")
            if status == "INVALID_REQUEST" and next_page_token:
                continue

            if status not in ("OK", "ZERO_RESULTS"):
                raise ValueError(f"Google API error: {data}")

            break
        else:
            raise ValueError("Google API next_page_token never became ready")

        results.extend(data.get("results", []))
        next_page_token = data.get("next_page_token")

        if not next_page_token or status == "ZERO_RESULTS":
            break

    return results


def _generate_grid_centers(bounds, target_spacing_meters=700):
    lat_step = target_spacing_meters / 111_320
    average_lat = (bounds["north"] + bounds["south"]) / 2
    lng_step = target_spacing_meters / (111_320 * max(0.2, math.cos(math.radians(average_lat))))

    centers = []
    lat = bounds["south"]
    while lat <= bounds["north"]:
        lng = bounds["west"]
        while lng <= bounds["east"]:
            centers.append((round(lat, 6), round(lng, 6)))
            lng += lng_step
        lat += lat_step

    return centers


def fetch_williamsburg_bars(max_search_centers=MAX_SEARCH_CENTERS, radius=700):
    centers = _generate_grid_centers(WILLIAMSBURG_BOUNDS, target_spacing_meters=radius)

    print(
        f"Preparing Williamsburg fetch with {len(centers)} candidate centers; "
        f"using up to {max_search_centers}."
    )

    if len(centers) > max_search_centers:
        print(
            f"Reached the Williamsburg search-center limit of {max_search_centers}; "
            f"stopping after the first {max_search_centers} centers."
        )

    unique_places = {}

    for index, (lat, lng) in enumerate(centers[:max_search_centers], start=1):
        print(f"Fetching center {index}/{min(len(centers), max_search_centers)} at {lat}, {lng}")
        for place in fetch_places_paginated(lat=lat, lng=lng, radius=radius, place_type="bar"):
            place_id = place.get("place_id")
            if not place_id:
                continue
            unique_places[place_id] = place

    places = list(unique_places.values())
    print(f"Fetched {len(places)} unique places.")
    return places
