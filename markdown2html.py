#!/usr/bin/python3
"""
markdown2html.py

Checks command-line arguments and validates the existence
of a Markdown file before HTML conversion.
"""

import sys
import os


def main():
    """Function that validates arguments and input file."""
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
        )
        sys.exit(1)

    markdown_file = sys.argv[1]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
