import sys
import argparse
import threading
from retainium import color

class Diagnostics:
    """Handles logging of errors, warnings, notes, and debug messages."""

    _debug_enabled = False  # Controls debug output
    _lock = threading.Lock()  # Ensures thread-safe output

    @classmethod
    def enable_debug(cls, enabled: bool):
        """Enables or disables debug output based on CLI flag."""
        cls._debug_enabled = enabled

    @classmethod
    def is_debug_enabled(cls) -> bool:
        """Query if debug mode is enabled or not."""
        return cls._debug_enabled

    @classmethod
    def diagnostic(cls, severity: str, message: str):
        """Prints a diagnostic message with a given severity."""
        if severity == "debug" and not cls._debug_enabled:
            return  # Skip debug messages unless debugging is enabled

        color_code = color.TerminalColors.get_color(severity)
        reset = color.TerminalColors.get_color("reset")
        formatted_message = f"{color_code}{severity}: {message}.{reset}"

        with cls._lock:  # Thread-safe printing
            print(formatted_message, file=sys.stderr)

    @classmethod
    def error(cls, message: str):
        cls.diagnostic("error", message)

    @classmethod
    def warning(cls, message: str):
        cls.diagnostic("warning", message)

    @classmethod
    def note(cls, message: str):
        cls.diagnostic("note", message)

    @classmethod
    def debug(cls, message: str):
        cls.diagnostic("debug", message)

    @classmethod
    def success(cls, message: str):
        cls.diagnostic("success", message)

    # Demo all diagnostics with color selections
    @classmethod
    def demo(cls):
        cls.error("this is an error")
        cls.warning("this is a warning")
        cls.note("this is a note")
        cls.debug("this is a debug message (won't show unless debug is enabled)")
        cls.success("this is success message")
