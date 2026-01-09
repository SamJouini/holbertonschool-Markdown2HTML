#!/usr/bin/python3
"""
markdown2html.py

Checks command-line arguments and validates the existence
of a Markdown file then do HTML conversion.

"""

import sys
import os

def convert_to_html(md_content):
    """
    Convert Markdown headers (# item), unordered lists (- item) and
    ordered lists (* item) to HTML format.
    """

    html_lines = []
    ul_list = False
    ol_list = False

    # Remove potential space before the item
    for line in md_content:
        stripped = line.lstrip()

        # For headers
        if stripped.startswith('#'):

            # Close any open lists
            if ul_list:
                html_lines.append("</ul>")
                ul_list = False
            if ol_list:
                html_lines.append("</ol>")
                ol_list = False

            level = 0
            while level < len(stripped) and stripped[level] == '#':
                level += 1
            heading_text = stripped[level:].lstrip()
            html_lines.append(f"<h{level}>{heading_text}</h{level}>")

        # For Unordered lists
        elif stripped.startswith('- '):
            # Close ordered list if open
            if ol_list:
                html_lines.append("</ol>")
                ol_list = False
            if not ul_list:
                html_lines.append("<ul>")
                ul_list = True
            html_lines.append(f"<li>{stripped[2:].strip()}</li>")

        # For Ordered lists
        elif stripped.startswith('* '):
            # Close unordered list if open
            if ul_list:
                html_lines.append("</ul>")
                ul_list = False
            if not ol_list:
                html_lines.append("<ol>")
                ol_list = True
            html_lines.append(f"<li>{stripped[2:].strip()}</li>")

        # Other situations
        else:
            if ul_list:
                html_lines.append("</ul>")
                ul_list = False
            if ol_list:
                html_lines.append("</ol>")
                ol_list = False
            # ignore other lines

    # Close any open lists at EOF
    if ul_list:
        html_lines.append("</ul>")
    if ol_list:
        html_lines.append("</ol>")

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

    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_lines = f.readlines()

    html_lines = convert_to_html(md_lines)

    with open(html_file, 'w', encoding='utf-8') as f:
        for line in html_lines:
            f.write(line + '\n')

    sys.exit(0)

if __name__ == "__main__":
    main()
