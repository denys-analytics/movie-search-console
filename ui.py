"""
NEO UI — unified module for styling the console interface.
"""

from config import UI_WIDTH as WIDTH


def ui_line(char="─"):
    return char * WIDTH


def ui_header(title: str):
    print("┌" + ui_line("─") + "┐")
    print("│" + title.center(WIDTH) + "│")
    print("└" + ui_line("─") + "┘")


def ui_block(lines: list[str]):
    print("┌" + ui_line("─") + "┐")
    for line in lines:
        print("│ " + line.ljust(WIDTH - 2) + " │")
    print("└" + ui_line("─") + "┘")


def ui_block_dynamic(lines: list[str], width: int):
    """Block whose width matches the table width."""
    print("┌" + "─" * width + "┐")
    for line in lines:
        print("│ " + line.ljust(width - 2) + " │")
    print("└" + "─" * width + "┘")


def ui_info(text: str):
    print(f"• {text}")


def ui_success(text: str):
    print(f"✓ {text}")


def ui_error(text: str):
    print(f"! {text}")
