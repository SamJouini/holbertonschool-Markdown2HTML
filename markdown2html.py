#!/usr/bin/python3
"""
markdown2html.py

Checks command-line arguments and validates the existence
of a Markdown file then do HTML conversion.

"""

import sys
import os
import hashlib

def format_conversion(text):
    """
    Convert Markdown bold (**text**), italic (__text__) , MD5 [[text]] 
    and remove c/C  ((text)) with HTML tags.
    """

    # Replace bold: **text** with <b>text</b>
    while '**' in text:
        start = text.find('**')
        end = text.find('**', start + 2)
        if start != -1 and end != -1:
            text = text[:start] + '<b>' + text[start+2:end] + '</b>' + text[end+2:]
        else:
            break

    # Replace italic: __text__ with <em>text</em>
    while '__' in text:
        start = text.find('__')
        end = text.find('__', start + 2)
        if start != -1 and end != -1:
            text = text[:start] + '<em>' + text[start+2:end] + '</em>' + text[end+2:]
        else:
            break

    # Replace: [[text]] to MD5 hash
    while '[[' in text:
        start = text.find('[[')
        end = text.find(']]', start + 2)
        if start != -1 and end != -1:
            content = text[start + 2:end]
            md5_hash = hashlib.md5(content.encode()).hexdigest()
            text = text[:start] + md5_hash + text[end + 2:]
        else:
            break

    # Replace ((text)) by removing c/C
    while '((' in text:
        start = text.find('((')
        end = text.find('))', start + 2)
        if start != -1 and end != -1:
            content = text[start + 2:end]
            filtered = ''.join(ch for ch in content if ch.lower() != 'c')
            text = text[:start] + filtered + text[end + 2:]
        else:
            break

    return text

def convert_to_html(md_content):
    """
    Convert Markdown headers (# item), unordered lists (- item) and
    ordered lists (* item) to HTML format.
    """

    html_lines = []
    ul_list = False
    ol_list = False
    in_paragraph = False

    # Remove potential space before the item
    for line in md_content:
        stripped = line.lstrip()

        # Skip completely empty lines but close paragraph if open
        if not stripped:
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            continue

        # For headers
        if stripped.startswith('#'):

            # Close any open lists or paragraph
            if ul_list:
                html_lines.append("</ul>")
                ul_list = False
            if ol_list:
                html_lines.append("</ol>")
                ol_list = False
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False

            level = 0
            while level < len(stripped) and stripped[level] == '#':
                level += 1
            heading_text = stripped[level:].lstrip()
            html_lines.append(f"<h{level}>{heading_text}</h{level}>")

        # For Unordered lists
        elif stripped.startswith('- '):
            # Close ordered list or paragraph if open
            if ol_list:
                html_lines.append("</ol>")
                ol_list = False
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if not ul_list:
                html_lines.append("<ul>")
                ul_list = True
            html_lines.append(f"<li>{stripped[2:].strip()}</li>")

        # For Ordered lists
        elif stripped.startswith('* '):
            # Close unordered list or paragraph if open
            if ul_list:
                html_lines.append("</ul>")
                ul_list = False
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if not ol_list:
                html_lines.append("<ol>")
                ol_list = True
            html_lines.append(f"<li>{stripped[2:].strip()}</li>")

        # For Paragraphes
        else:
            # Close ordered or unordered list if open
            if ul_list:
                html_lines.append("</ul>")
                ul_list = False
            if ol_list:
                html_lines.append("</ol>")
                ol_list = False
            if not in_paragraph:
                html_lines.append("<p>")
                in_paragraph = True
            html_lines.append(stripped)

    # Close any open items at EOF
    if ul_list:
        html_lines.append("</ul>")
    if ol_list:
        html_lines.append("</ol>")
    if in_paragraph:
        html_lines.append("</p>")

    return html_lines

def main():
    """Function that validates arguments and input file."""
    if len(sys.argv) != 3:
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

    # Handle headers, lists and paragraphes
    html_lines = convert_to_html(md_lines)

    # Handle text format (bolld and italics)
    html_lines = [format_conversion(line) for line in html_lines]

    with open(html_file, 'w', encoding='utf-8') as f:
        for line in html_lines:
            f.write(line + '\n')

    sys.exit(0)

if __name__ == "__main__":
    main()
