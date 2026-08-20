"""
Utility module with helper functions for validating user input.
Used in the UI to safely receive data from the user.
"""

import re

# ============================================================
#   READ INTEGER

def read_int(prompt: str) -> int:
    """Request an integer from the user."""
    while True:
        value = input(prompt).strip()
        if re.fullmatch(r"-?\d+", value):
            return int(value)
        print("Error: please enter an integer.")


# ============================================================
#   READ INTEGER WITH RANGE LIMITS

def read_int_range(prompt: str, min_value: int, max_value: int) -> int:
    """Request an integer within the range [min_value, max_value]."""
    while True:
        value = read_int(prompt)
        if min_value <= value <= max_value:
            return value
        print(f"Error: number must be between {min_value} and {max_value}.")


# ============================================================
#   MENU CHOICE

def input_menu_choice(prompt: str, choices: list[int]) -> int:
    """Request a menu option from the user."""
    while True:
        value = input(prompt).strip()

        if value.startswith("0") and value != "0":
            print("Error: invalid number format!")
            continue

        if value.isdigit():
            num = int(value)
            if num in choices:
                return num

        print(f"Error: choose one of the options: {choices}")


# ============================================================
#   PAGINATION COMMANDS

def input_pagination_command(prompt: str, commands: list[str]) -> str:
    """Request a pagination command."""
    while True:
        value = input(prompt).strip().lower()
        if value in commands:
            return value
        print(f"Error: valid commands are: {', '.join(commands)}")


# ============================================================
#   NON-EMPTY STRING

def read_non_empty(prompt: str) -> str:
    """Request a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: string cannot be empty!")


# ============================================================
#   SIMPLE TEXT INPUT

def input_text(prompt: str) -> str:
    """Allows input of English letters, digits, spaces, and hyphens."""
    pattern = re.compile(r"^[A-Za-z0-9\s\-]+$")

    while True:
        value = input(prompt).strip()

        if not value:
            print("Error: string cannot be empty!")
            continue

        if not pattern.fullmatch(value):
            print("Error: only English letters, digits, spaces, and hyphens are allowed!")
            continue

        return value


# ============================================================
#   READ STRING OR EMPTY VALUE

def read_optional(prompt: str) -> str | None:
    """Request a string; empty input returns None."""
    value = input(prompt).strip()
    return value if value else None
