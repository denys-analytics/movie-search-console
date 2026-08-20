"""
Global project settings and constants.
All parameters are grouped by subsystems.
This version is safe for GitHub: no passwords, no server URIs.
All sensitive data is loaded from environment variables.
"""

import os

# ============================================================
#   MongoDB (Primary Database)

# Connection string is taken from environment variable MONGO_URI.
# Example (in .env or system environment):
# MONGO_URI="mongodb+srv://db_user:db_password@cluster0.example.mongodb.net/movie_db?retryWrites=true&w=majority"

MONGO_URI: str = os.getenv("MONGO_URI", "")

# Main database name (can be changed for any MongoDB deployment)
MONGO_DB: str = os.getenv("MONGO_DB", "movie_db")

# Collections used in the project (fully customizable)
MONGO_COLLECTION_FILMS: str = os.getenv("MONGO_COLLECTION_FILMS", "films")
MONGO_COLLECTION_CATEGORIES: str = os.getenv("MONGO_COLLECTION_CATEGORIES", "categories")
MONGO_COLLECTION_FILM_CATEGORY: str = os.getenv("MONGO_COLLECTION_FILM_CATEGORY", "film_category")

# Logging collection (optional)
MONGO_COLLECTION_LOGS: str = os.getenv("MONGO_COLLECTION_LOGS", "search_events")

# Timezone for logging
TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Berlin")


# ============================================================
#   UI + Pagination

PAGE_SIZE: int = int(os.getenv("PAGE_SIZE", 10))
UI_WIDTH: int = int(os.getenv("UI_WIDTH", 60))
