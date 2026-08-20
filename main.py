"""Main module of the console application for movie search."""

from mongo_connector import (
    search_by_keyword,
    search_by_genre_and_years,
    search_by_rating,
    get_genres,
)

from log_writer import (
    log_search,
    get_collection,
    close_mongo,
)

from log_stats import (
    show_top_keywords,
    show_top_genre_years,
    show_top_rating,
    show_top_last,
)

from formatter import print_table

from utils import (
    input_menu_choice,
    input_text,
    input_pagination_command,
    read_int,
    read_int_range,
)

from ui import (
    ui_header,
    ui_block,
    ui_block_dynamic,
    ui_info,
    ui_success,
    ui_error,
)

from config import PAGE_SIZE


# ============================================================
#   UNIVERSAL PAGINATION

def paginate_results(
    results: list[list[object]],
    title: str = "Search Results",
    headers: list[str] | None = None
) -> None:
    """Universal pagination."""

    if not results:
        ui_error("No results found")
        return

    if headers is None:
        headers = ["№", "Title", "Year", "Genre", "Rating"]

    page = 0
    total_pages = (len(results) - 1) // PAGE_SIZE + 1

    while True:

        start = page * PAGE_SIZE
        end = start + PAGE_SIZE
        page_results = results[start:end]

        numbered_rows = []
        for idx, row in enumerate(page_results):
            number = idx + 1 + page * PAGE_SIZE
            new_row = (number,) + tuple(row[1:])
            numbered_rows.append(new_row)

        total_width = print_table(
            headers=headers,
            rows=numbered_rows,
            title=f"{title} — page {page + 1} of {total_pages}",
            return_width=True,
        )

        commands = ["Available commands:"]

        if total_pages == 1:
            commands.append("This is the only page")
            commands.append("0  return to menu")
            ui_block_dynamic(commands, total_width)
            input_pagination_command(
                prompt="Press 0 to exit: ",
                commands=["0"]
            )
            return

        if page == 0:
            commands.append("+  next")
            commands.append("0  return to menu")
            prompt = "Choose an action [+ / 0]: "

        elif page == total_pages - 1:
            commands.append("This is the last page")
            commands.append("-  previous")
            commands.append("0  return to menu")
            prompt = "Choose an action [- / 0]: "

        else:
            commands.append("+  next")
            commands.append("-  previous")
            commands.append("0  return to menu")
            prompt = "Choose an action [+ / - / 0]: "

        ui_block_dynamic(commands, total_width)

        cmd = input_pagination_command(prompt=prompt, commands=["+", "-", "0"])

        if cmd == "+" and page < total_pages - 1:
            page += 1
        elif cmd == "-" and page > 0:
            page -= 1
        elif cmd == "0":
            return
        else:
            ui_info("Unavailable command")


# ============================================================
#   UNIVERSAL SEARCH RUNNER

def run_search(
    search_func,
    search_type: str,
    params: dict,
    *args,
    title: str = "Search Results"
) -> None:
    """Universal search runner with logging and pagination."""

    results = search_func(*args)

    ui_info(f"Found: {len(results)}")

    log_search(
        search_type=search_type,
        params=params,
        results_count=len(results),
    )

    paginate_results(results, title=title)


# ============================================================
#   MPAA RATINGS

RATINGS = [
    ("G",     "General Audiences — suitable for all",               "0+"),
    ("PG",    "Parental Guidance Suggested — some material may not be suitable", "10+"),
    ("PG-13", "Parents Strongly Cautioned — not suitable under 13", "13+"),
    ("R",     "Restricted — under 17 requires accompanying parent", "17+"),
    ("NC-17", "Adults Only — strictly 18+",                         "18+"),
]


# ============================================================
#   SEARCH MENUS

def menu_search_keyword() -> None:
    keyword = input_text("Enter a keyword or movie title: ")

    ui_info(f"Searching for '{keyword}'...")

    run_search(
        search_by_keyword,
        "search_keyword",
        {"keyword": keyword},
        keyword,
        title=f"Search: {keyword}",
    )


def menu_search_genre_years() -> None:
    genres = get_genres()

    table_rows = []
    for genre_id, genre_name, min_year, max_year in genres:
        years = f"{min_year}–{max_year}" if min_year is not None else "No data"
        table_rows.append([genre_id, genre_name, years])

    print_table(
        headers=["ID", "Genre", "Years"],
        rows=table_rows,
        title="Available Genres",
    )

    genre_id = read_int("Enter genre ID: ")

    genre_dict = {gid: (name, min_y, max_y) for gid, name, min_y, max_y in genres}

    if genre_id not in genre_dict:
        ui_error("No genre with this ID")
        return

    genre_name, min_year, max_year = genre_dict[genre_id]

    if min_year is None:
        ui_error("No films available for this genre")
        return

    ui_block([
        f'Available year range for genre "{genre_name}":',
        f"Minimum year: {min_year}",
        f"Maximum year: {max_year}",
    ])

    year_from = read_int_range(
        f"Enter start year (from {min_year}): ",
        min_year,
        max_year,
    )

    while True:
        year_to = read_int_range(
            f"Enter end year (up to {max_year}): ",
            min_year,
            max_year,
        )

        if year_to < year_from:
            ui_error("Error: end year cannot be less than start year")
            continue

        break

    run_search(
        search_by_genre_and_years,
        "search_genre_years",
        {
            "category_id": genre_id,
            "category_name": genre_name,
            "year_from": year_from,
            "year_to": year_to,
        },
        genre_id,
        year_from,
        year_to,
        title=f"{genre_name} ({year_from}–{year_to})",
    )


def menu_search_rating() -> None:
    table_rows = []
    for idx, (code, desc, age) in enumerate(RATINGS, start=1):
        table_rows.append([idx, code, desc, age])

    print_table(
        headers=["№", "Code", "Description", "Age"],
        rows=table_rows,
        title="MPAA Ratings",
    )

    choice = read_int_range("Enter rating number (1–5): ", 1, 5)
    rating_code = RATINGS[choice - 1][0]

    run_search(
        search_by_rating,
        "search_rating",
        {"rating": rating_code},
        rating_code,
        title=f"Rating: {rating_code}",
    )


def ui_stats_menu(collection) -> None:
    while True:
        ui_header("QUERY STATISTICS (MongoDB)")

        ui_block([
            "1 - TOP-5 keyword searches",
            "2 - TOP-5 genre/year searches",
            "3 - TOP-5 rating searches",
            "4 - TOP-5 latest unique queries",
            "0 - Return to menu",
        ])

        choice = input_menu_choice("Choose an option: ", [0, 1, 2, 3, 4])

        if choice == 0:
            return
        elif choice == 1:
            show_top_keywords(collection)
        elif choice == 2:
            show_top_genre_years(collection)
        elif choice == 3:
            show_top_rating(collection)
        elif choice == 4:
            show_top_last(collection)


# ============================================================
#   MAIN MENU

def main() -> None:
    ui_header("INITIALIZATION")

    mongo = get_collection()
    ui_success("Connected to MongoDB")

    print()

    try:
        while True:
            ui_header("MENU")

            ui_block([
                "1 - Search by movie title",
                "2 - Search by genre and year range",
                "3 - Search by rating",
                "4 - Statistics",
                "0 - Exit",
            ])

            choice = input_menu_choice("Choose an option: ", [0, 1, 2, 3, 4])

            if choice == 0:
                ui_header("SHUTTING DOWN")
                break
            elif choice == 1:
                menu_search_keyword()
            elif choice == 2:
                menu_search_genre_years()
            elif choice == 3:
                menu_search_rating()
            elif choice == 4:
                ui_stats_menu(mongo)

    finally:
        close_mongo()

        ui_header("CLOSING CONNECTIONS")
        ui_success("MongoDB connection closed")
        ui_success("Program terminated.")


if __name__ == "__main__":
    main()
