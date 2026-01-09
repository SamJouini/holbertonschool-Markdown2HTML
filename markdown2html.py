#!/usr/bin/python3
"""
markdown2html.py

Checks command-line arguments and validates the existence
of a Markdown file before HTML conversion.

Currently, the sript only converts headings.
"""

import sys
import os

def convert_headings_to_html(md_content):
    """
    Convert Markdown headings (# to ######) to HTML <h1> to <h6>.

    Args:
        md_content (list of str): Lines of Markdown text

    Returns:
        list of str: Lines of HTML text
    """

    html_lines = []

    for line in md_content:
        if line.startswith('#'):
            # Count the number of '#' at the start (heading level)
            level = 0
            while level < len(line) and line[level] == '#':
                level += 1
            # Only consider headings level 1-6
            if 1 <= level <= 6:
                # Remove leading '#' and possible space
                heading_text = line[level:].lstrip()
                html_lines.append(f"<h{level}>{heading_text}</h{level}>")
    return html_lines

def main():
    """Function that validates arguments and input file."""
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
        )
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_lines = f.readlines()

    html_lines = convert_headings_to_html(md_lines)

    with open(html_file, 'w', encoding='utf-8') as f:
        for line in html_lines:
            f.write(line + '\n')

    sys.exit(0)

if __name__ == "__main__":
    main()
