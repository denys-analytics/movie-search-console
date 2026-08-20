"""
Module for query statistics (MongoDB).

Uses log entries with the structure:
- event: str
- data: dict
- timestamp: ISO string

Provides:
- TOP-N by keyword
- TOP-N by genre and year range
- TOP-N by rating
- latest unique queries
"""

from formatter import print_table
from pymongo.collection import Collection


# ============================================================
#   HELPER FUNCTIONS

def format_params(params: dict | str, max_len: int = 60) -> str:
    """Format parameters into a single trimmed string."""
    if isinstance(params, dict):
        text = ", ".join(f"{k}: {v}" for k, v in params.items())
    else:
        text = str(params)

    return text if len(text) <= max_len else text[:max_len - 3] + "..."


# ============================================================
#   TOP-N BY KEYWORD

def show_top_keywords(collection: Collection, limit: int = 5) -> None:
    pipeline = [
        {"$match": {"event": "search_keyword"}},
        {"$group": {
            "_id": "$data.keyword",
            "count": {"$sum": 1},
            "last_ts": {"$max": "$timestamp"},
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit},
    ]

    results = list(collection.aggregate(pipeline))

    rows = [
        [idx, row["_id"], row["count"], row["last_ts"]]
        for idx, row in enumerate(results, start=1)
    ]

    print_table(
        headers=["№", "Keyword", "Count", "Last Query"],
        rows=rows,
        title=f"TOP-{limit} most popular keyword searches",
    )


# ============================================================
#   TOP-N BY GENRE AND YEAR RANGE

def show_top_genre_years(collection: Collection, limit: int = 5) -> None:
    pipeline = [
        {"$match": {"event": "search_genre_years"}},
        {"$group": {
            "_id": {
                "category_name": "$data.category_name",
                "year_from": "$data.year_from",
                "year_to": "$data.year_to",
            },
            "count": {"$sum": 1},
            "last_ts": {"$max": "$timestamp"},
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit},
    ]

    results = list(collection.aggregate(pipeline))

    rows = []
    for idx, row in enumerate(results, start=1):
        g = row["_id"]
        genre = g.get("category_name", "?")
        years = f"{g.get('year_from', '?')}–{g.get('year_to', '?')}"
        rows.append([idx, genre, years, row["count"], row["last_ts"]])

    print_table(
        headers=["№", "Genre", "Years", "Count", "Last Query"],
        rows=rows,
        title=f"TOP-{limit} most popular genre/year searches",
    )


# ============================================================
#   TOP-N BY RATING

def show_top_rating(collection: Collection, limit: int = 5) -> None:
    pipeline = [
        {"$match": {"event": "search_rating"}},
        {"$group": {
            "_id": "$data.rating",
            "count": {"$sum": 1},
            "last_ts": {"$max": "$timestamp"},
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit},
    ]

    results = list(collection.aggregate(pipeline))

    rows = [
        [idx, row["_id"], row["count"], row["last_ts"]]
        for idx, row in enumerate(results, start=1)
    ]

    print_table(
        headers=["№", "Rating", "Count", "Last Query"],
        rows=rows,
        title=f"TOP-{limit} most popular rating searches",
    )


# ============================================================
#   LATEST UNIQUE QUERIES

def show_top_last(collection: Collection, limit: int = 5) -> None:
    TYPE_NAMES = {
        "search_keyword": "Keyword Search",
        "search_rating": "Rating Search",
        "search_genre_years": "Genre/Years Search",
    }

    all_logs = list(collection.find())
    unique = {}

    for log in all_logs:
        if "event" not in log or "data" not in log or "timestamp" not in log:
            continue

        key = (log["event"], str(log["data"]))
        if key not in unique or log["timestamp"] > unique[key]["timestamp"]:
            unique[key] = log

    unique_logs = sorted(unique.values(), key=lambda x: x["timestamp"], reverse=True)[:limit]

    rows = []
    for idx, log in enumerate(unique_logs, start=1):
        event = log["event"]
        params = log["data"]
        type_name = TYPE_NAMES.get(event, event)

        if event == "search_keyword":
            param_text = params.get("keyword", "?")
        elif event == "search_rating":
            param_text = params.get("rating", "?")
        elif event == "search_genre_years":
            genre = params.get("category_name", "?")
            y1 = params.get("year_from", "?")
            y2 = params.get("year_to", "?")
            param_text = f"{genre} ({y1}–{y2})"
        else:
            param_text = format_params(params)

        results_count = params.get("results_count", "?")

        rows.append([idx, type_name, param_text, results_count, log["timestamp"]])

    print_table(
        headers=["№", "Type", "Parameters", "Results", "Time"],
        rows=rows,
        title=f"TOP-{limit} latest unique queries",
    )
