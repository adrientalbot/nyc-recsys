# NYC Recsys

This project fetches Google Places data for Williamsburg bars, combines it with a saved-places list, and trains a simple ranking model to score which places are most likely to fit the user’s taste.

## What it does

- Fetches bar data from the Google Places Nearby Search API
- Caches the fetched results in `data/fetched_places.json`
- Loads the user’s saved places from `data/Saved Places.json`
- Builds a feature set from the fetched places
- Trains a logistic regression model
- Prints the top scored recommendations

## Setup

1. Clone the repo.
2. Add your Google Places API key to `.env`:

```env
GOOGLE_PLACES_API_KEY=your_key_here
```

3. Sync the environment:

```bash
uv sync
```

## Usage

Fetch and cache fresh Williamsburg places:

```bash
uv run python fetch_places.py
```

Train and score using the cached data:

```bash
uv run python train_and_score.py
```

Force a fresh fetch before training and scoring:

```bash
uv run python train_and_score.py --refresh-data
```

## Notes

- If `data/fetched_places.json` is missing, `train_and_score.py` will fetch fresh data automatically.
- The fetched data is cached so repeated scoring runs do not hit the Google API unless you request a refresh.
- `data/Saved Places.json` is the saved-places source used to label and filter recommendations.

## Next Steps

- Remove the need to manually upload the saved-places JSON file by pulling that data directly from Google in a supported way.
- Build a simple UI for running the scorer and viewing the ranked results.
