from app.services.places import fetch_places
from app.services.dataset import build_dataset, load_saved_places
from app.services.model import train_model, score_places

# fetch
places = fetch_places()

# dataset
X, y, places = build_dataset(places)
saved = load_saved_places()

# train
model = train_model(X, y)

# score
results = score_places(model, X, places, exclude_names=saved)

# print top 10
for r in results[:10]:
    print(f"{r['name']} - {r['score']} - {r['rating']}")
