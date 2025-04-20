# Copyright (C) 2024-2025 Soumitra Chatterjee
# Licensed under the GNU AGPL-3.0. See LICENSE file for details.

# Modular implementation of color capabilities

class TerminalColors:
    """Encapsulates ANSI color codes and severity-based themes."""

    # ANSI escape codes (can be customized)
    COLORS = {
        "black": "\033[30m",
        "red": "\033[91m",
        "amber": "\033[38;5;214m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "teal": "\033[36m",
        "dark_teal": "\033[38;5;30m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }

    # Default severity mapping (can be changed at runtime)
    SEVERITY_THEME = {
        "error": COLORS["red"],          # Deep red
        "warning": COLORS["amber"],      # Amber/light red
        "note": COLORS["dark_teal"],     # Dark teal
        "success": COLORS["green"],      # Green
        "debug": COLORS["magenta"],
        "reset": COLORS["reset"]
    }

    @classmethod
    def get_color(cls, severity: str) -> str:
        return cls.SEVERITY_THEME.get(severity.lower(), cls.COLORS["reset"])

    @classmethod
    def set_color(cls, severity: str, ansi_code: str):
        cls.SEVERITY_THEME[severity.lower()] = ansi_code

    @classmethod
    def reset_theme(cls):
        """Resets the theme to default values."""
        cls.SEVERITY_THEME.update({
            "error": cls.COLORS["red"],
            "warning": cls.COLORS["amber"],
            "note": cls.COLORS["dark_teal"],
            "debug": cls.COLORS["magenta"],
            "reset": cls.COLORS["reset"]
        })

