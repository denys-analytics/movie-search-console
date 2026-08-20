"""
Table formatting module for the console UI.
Uses dynamic column width calculation.
"""

def print_table(
    headers: list[str],
    rows: list[list],
    title: str = "",
    return_width: bool = False
) -> int | None:
    """
    Print a formatted table in UI style.
    If return_width = True — returns the total table width.
    """

    # ============================================================
    #   COLUMN WIDTH CALCULATION

    col_widths = []
    for col_index, header in enumerate(headers):
        max_len = max(
            (len(str(row[col_index])) for row in rows),
            default=0
        )
        width = max(max_len, len(header)) + 2
        col_widths.append(width)

    total_width = sum(col_widths) + len(headers) - 1

    # ============================================================
    #   TABLE TITLE

    if title:
        print("┌" + "─" * total_width + "┐")
        print("│" + title.center(total_width) + "│")
        print("└" + "─" * total_width + "┘")

    # ============================================================
    #   TOP BORDER

    print("┌" + "┬".join("─" * w for w in col_widths) + "┐")

    # ============================================================
    #   HEADERS

    header_cells = [header.center(col_widths[i]) for i, header in enumerate(headers)]
    print("│" + "│".join(header_cells) + "│")

    print("├" + "┼".join("─" * w for w in col_widths) + "┤")

    # ============================================================
    #   TABLE ROWS

    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            cell = str(cell)
            max_len = col_widths[i] - 1

            # trimming long values
            if len(cell) > max_len:
                cell = cell[: max_len - 1] + "…"

            # center numbers, left-align text
            if cell.replace("-", "").isdigit():
                cell = cell.center(col_widths[i])
            else:
                cell = cell.ljust(col_widths[i])

            cells.append(cell)

        print("│" + "│".join(cells) + "│")

    # ============================================================
    #   BOTTOM BORDER

    print("└" + "┴".join("─" * w for w in col_widths) + "┘")

    if return_width:
        return total_width
