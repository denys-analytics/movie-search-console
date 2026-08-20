"""
Module for connecting to MongoDB and logging events.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from pymongo import MongoClient
from pymongo.collection import Collection

from config import (
    TIMEZONE,
    MONGO_URI,
    MONGO_DB,
    MONGO_COLLECTION_LOGS,
)

# ============================================================
#   MONGO CONNECTION

_client: MongoClient | None = None
_collection: Collection | None = None


def get_collection() -> Collection:
    """Return the MongoDB collection for logging."""
    global _client, _collection

    if _collection is None:
        _client = MongoClient(MONGO_URI)
        db = _client[MONGO_DB]
        _collection = db[MONGO_COLLECTION_LOGS]

    return _collection


# ============================================================
#   GENERIC LOGGER

def log_event(event: str, data: dict) -> None:
    """Write an event to MongoDB."""
    collection = get_collection()

    doc = {
        "timestamp": datetime.now(ZoneInfo(TIMEZONE)).isoformat(),
        "event": event,
        "data": data,
    }

    collection.insert_one(doc)


# ============================================================
#   LATEST LOGS

def last_logs(n: int) -> list[dict]:
    """Return the latest n log entries."""
    collection = get_collection()
    return list(collection.find().sort("timestamp", -1).limit(n))


# ============================================================
#   EVENT TYPE STATISTICS

def stats_by_event() -> list[dict]:
    """Return statistics grouped by event type."""
    collection = get_collection()

    pipeline = [
        {"$group": {"_id": "$event", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]

    return list(collection.aggregate(pipeline))


# ============================================================
#   LOGS BY SPECIFIC EVENT

def logs_by_event(event: str) -> list[dict]:
    """Return logs for a specific event type."""
    collection = get_collection()
    return list(collection.find({"event": event}).sort("timestamp", -1))


# ============================================================
#   SEARCH LOGGING

def log_search(search_type: str, params: dict, results_count: int) -> None:
    """Log a search query with parameters and results count."""
    data = params.copy()
    data["results_count"] = results_count
    log_event(search_type, data)


# ============================================================
#   CLOSE CONNECTION

def close_mongo() -> None:
    """Close the MongoDB client."""
    global _client, _collection

    if _client is not None:
        try:
            _client.close()
        except Exception:
            pass

    _client = None
    _collection = None
