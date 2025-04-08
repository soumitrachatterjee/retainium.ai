import argparse
from retainium.diagnostics import Diagnostics
from retainium.color import TerminalColors

def demo_colors():
    print("\n---- Color Demo ----\n")
    Diagnostics.note("this is a note")
    Diagnostics.warning("this is a warning")
    Diagnostics.error("this is an error")
    Diagnostics.debug("this is a debug message (won't show unless debug is enabled)")

    print("\nTip: Use `TerminalColors.set_color()` to tweak themes dynamically.")

def main():
    parser = argparse.ArgumentParser(description="Retainium Color Demo")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    Diagnostics.enable_debug(args.debug)
    demo_colors()

if __name__ == "__main__":
    main()

