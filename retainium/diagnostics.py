import sys
import threading
from retainium import color

###
## Example tweaks
#from retainium.color import TerminalColors
#TerminalColors.set_color("note", "\033[92m")  # Set note to green
###

class Diagnostics:
    """Handles logging of errors, warnings, notes, and debug messages."""

    _debug_enabled = False
    _lock = threading.Lock()

    @classmethod
    def enable_debug(cls, enabled: bool):
        cls._debug_enabled = enabled

    @classmethod
    def diagnostic(cls, severity: str, message: str):
        if severity == "debug" and not cls._debug_enabled:
            return

        color_code = color.TerminalColors.get_color(severity)
        reset = color.TerminalColors.get_color("reset")
        formatted = f"{color_code}{severity}: {message}.{reset}"

        with cls._lock:
            print(formatted, file=sys.stderr)

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
