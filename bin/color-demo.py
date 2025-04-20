# Copyright (C) 2024-2025 Soumitra Chatterjee
# Licensed under the GNU AGPL-3.0. See LICENSE file for details.

# Enable relative module lookups
# (protect against symlinks using realpath())
import os, sys
root = os.path.realpath(os.path.dirname(__file__) + "/..")
if root not in sys.path:
    sys.path.insert(0, root)

# Import required modules
import argparse
from retainium.diagnostics import Diagnostics
from retainium.color import TerminalColors

# Demo colored diagnostics capabilities
def demo_colors():
    print("\n---- Diagnostics Color Demo ----\n")
    Diagnostics.demo()
    print("\nTip: Use `TerminalColors.set_color()` to tweak themes dynamically.")

def main():
    parser = argparse.ArgumentParser(description="Retainium Color Demo")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    Diagnostics.enable_debug(args.debug)
    demo_colors()

if __name__ == "__main__":
    main()

