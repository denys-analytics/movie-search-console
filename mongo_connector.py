"""
MongoDB connector module for film search.
Replaces MySQL logic completely.
"""

from pymongo import MongoClient
from config import (
    MONGO_URI,
    MONGO_DB,
    MONGO_COLLECTION_FILMS,
    MONGO_COLLECTION_CATEGORIES,
    MONGO_COLLECTION_FILM_CATEGORY,
)

# ============================================================
#   CONNECTION

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

films = db[MONGO_COLLECTION_FILMS]
categories = db[MONGO_COLLECTION_CATEGORIES]
film_category = db[MONGO_COLLECTION_FILM_CATEGORY]

# ============================================================
#   AUTO-FIX release_year (convert string → int)
# ============================================================

def fix_release_years():
    fixed = 0
    for doc in films.find({}):
        year = doc.get("release_year")
        if isinstance(year, str):
            try:
                films.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"release_year": int(year)}}
                )
                fixed += 1
            except:
                pass
    if fixed > 0:
        print(f"[MongoDB] Fixed release_year for {fixed} films.")


# Run auto-fix on module import
fix_release_years()

# ============================================================
#   FORMATTER (same output structure as MySQL version)

def _format(doc, category=None):
    return [
        doc.get("film_id"),
        doc.get("title"),
        doc.get("release_year"),
        category,
        doc.get("rating"),
    ]


# ============================================================
#   SEARCH BY KEYWORD

def search_by_keyword(keyword: str) -> list[list]:
    query = {"title": {"$regex": keyword, "$options": "i"}}
    results = list(films.find(query))

    formatted = []
    for doc in results:
        formatted.append(_format(doc))
    return formatted


# ============================================================
#   SEARCH BY RATING

def search_by_rating(rating: str) -> list[list]:
    results = list(films.find({"rating": rating}))

    formatted = []
    for doc in results:
        formatted.append(_format(doc))
    return formatted


# ============================================================
#   GENRE LIST WITH YEAR RANGE

def get_genres() -> list[tuple[int, str, int, int]]:
    genres = list(categories.find({}))
    result = []

    for g in genres:
        cat_id = g["category_id"]
        name = g["name"]

        # find films for this genre
        fc = list(film_category.find({"category_id": cat_id}))
        film_ids = [x["film_id"] for x in fc]

        years = list(films.find({"film_id": {"$in": film_ids}}, {"release_year": 1}))
        if years:
            min_year = min(int(x["release_year"]) for x in years)
            max_year = max(int(x["release_year"]) for x in years)

        else:
            min_year = None
            max_year = None

        result.append((cat_id, name, min_year, max_year))

    return result


# ============================================================
#   SEARCH BY GENRE + YEAR RANGE

def search_by_genre_and_years(
    genre_id: int,
    year_from: int,
    year_to: int
) -> list[list]:
    # find film_ids for this genre
    fc = list(film_category.find({"category_id": genre_id}))
    film_ids = [x["film_id"] for x in fc]

    query = {
        "film_id": {"$in": film_ids},
        "release_year": {"$gte": year_from, "$lte": year_to}
    }

    results = list(films.find(query))

    formatted = []
    for doc in results:
        formatted.append(_format(doc))
    return formatted
