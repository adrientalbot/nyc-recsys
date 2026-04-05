import json
from pathlib import Path

from app.services.features import extract_features


def load_saved_places():
    data_dir = Path("data")
    candidates = [
        data_dir / "saved_places.json",
        data_dir / "Saved Places.json",
    ]

    for path in candidates:
        if path.exists():
            with path.open() as f:
                payload = json.load(f)
            break
    else:
        raise FileNotFoundError("No saved places file found in data/")

    if isinstance(payload, list):
        return set(payload)

    features = payload.get("features", [])
    saved_names = set()

    for feature in features:
        name = (
            feature.get("properties", {})
            .get("location", {})
            .get("name")
        )
        if name:
            saved_names.add(name)

    return saved_names


def build_dataset(places):
    saved = load_saved_places()

    X = []
    y = []

    for place in places:
        features = extract_features(place)

        X.append(
            [
                features["rating"],
                features["price_level"],
                features["is_bar"],
                features["is_cafe"],
                features["is_restaurant"],
            ]
        )

        y.append(int(features["name"] in saved))

    return X, y, places
