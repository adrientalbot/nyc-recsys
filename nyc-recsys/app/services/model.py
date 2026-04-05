from sklearn.linear_model import LogisticRegression


def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    return model


def score_places(model, X, places, exclude_names=None):
    exclude_names = exclude_names or set()
    probs = model.predict_proba(X)[:, 1]

    results = []

    for place, prob in zip(places, probs):
        if place["name"] in exclude_names:
            continue
        results.append(
            {
                "name": place["name"],
                "score": float(prob),
                "rating": place.get("rating"),
            }
        )

    return sorted(results, key=lambda x: x["score"], reverse=True)
