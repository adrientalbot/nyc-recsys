def extract_features(place):
    types = place.get("types", [])

    return {
        "name": place.get("name"),
        "rating": place.get("rating", 0),
        "price_level": place.get("price_level", 0),
        "is_bar": int("bar" in types),
        "is_cafe": int("cafe" in types),
        "is_restaurant": int("restaurant" in types),
    }