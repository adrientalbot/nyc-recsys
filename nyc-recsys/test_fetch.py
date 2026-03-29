from app.services.places import fetch_places

places = fetch_places(place_type="restaurant")
print(f"Fetched {len(places)} places")

if places:
    print(places[0]["name"])