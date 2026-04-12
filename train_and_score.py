import argparse
import json
from pathlib import Path

from app.services.dataset import build_dataset, load_saved_places
from app.services.model import train_model, score_places
from app.services.places import fetch_williamsburg_bars

output_path = Path("data/fetched_places.json")


def load_fetched_places():
    if not output_path.exists():
        raise FileNotFoundError(
            f"{output_path} not found. Run `python3 fetch_places.py` first."
        )

    with output_path.open() as f:
        return json.load(f)


def refresh_fetched_places(max_search_centers=50):
    print("Refreshing fetched places...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    places = fetch_williamsburg_bars(max_search_centers=max_search_centers)
    print("Writing fetched places cache...")
    output_path.write_text(json.dumps(places, indent=2))
    print(f"Saved {len(places)} fetched places to {output_path}")
    return places


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh-data",
        action="store_true",
        help="Fetch fresh Google Places data before training and scoring",
    )
    args = parser.parse_args()

    if args.refresh_data or not output_path.exists():
        print("No cache found or refresh requested; fetching fresh data.")
        places = refresh_fetched_places()
    else:
        print("Loading fetched places from cache.")
        places = load_fetched_places()
        print(f"Loaded {len(places)} fetched places from {output_path}")

    print("Building dataset...")
    # dataset
    X, y, places = build_dataset(places)
    print("Loading saved places...")
    saved = load_saved_places()

    print("Training model...")
    # train
    model = train_model(X, y)

    print("Scoring places...")
    # score
    results = score_places(model, X, places, exclude_names=saved)

    print("Top results:")
    # print top 10
    for r in results[:10]:
        print(f"{r['name']} - {r['score']} - {r['rating']}")


if __name__ == "__main__":
    main()
