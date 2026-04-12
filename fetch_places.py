import argparse
import json
from pathlib import Path

from app.services.places import fetch_williamsburg_bars


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/fetched_places.json"),
        help="Path to write the fetched Google Places data",
    )
    parser.add_argument(
        "--max-search-centers",
        type=int,
        default=50,
        help="Maximum number of Williamsburg search centers to query",
    )
    args = parser.parse_args()

    places = fetch_williamsburg_bars(max_search_centers=args.max_search_centers)
    args.output.write_text(json.dumps(places, indent=2))
    print(f"Saved {len(places)} fetched places to {args.output}")


if __name__ == "__main__":
    main()
