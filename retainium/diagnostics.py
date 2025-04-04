import sys
import argparse
import threading

class Diagnostics:
    """Handles logging of errors, warnings, notes, and debug messages."""

    _debug_enabled = False  # Controls debug output
    _lock = threading.Lock()  # Ensures thread-safe output

    SEVERITY_COLORS = {
        "error": "\033[91m",    # Red
        "warning": "\033[93m",  # Yellow
        "note": "\033[96m",     # Cyan
        "debug": "\033[95m",    # Magenta
        "RESET": "\033[0m"      # Reset color
    }

    @classmethod
    def enable_debug(cls, enabled: bool):
        """Enables or disables debug output based on CLI flag."""
        cls._debug_enabled = enabled

    @classmethod
    def diagnostic(cls, severity: str, message: str):
        """Prints a diagnostic message with a given severity."""
        if severity == "debug" and not cls._debug_enabled:
            return  # Skip debug messages unless debugging is enabled

        color = cls.SEVERITY_COLORS.get(severity, cls.SEVERITY_COLORS["RESET"])
        formatted_message = f"{color}{severity}: {message}.{cls.SEVERITY_COLORS['RESET']}"

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
