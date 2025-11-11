#!/usr/bin/env python3
"""
Extract content from ministry.docx and convert to Markdown format.
Create separate files for each chapter.
"""

from docx import Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import Table
from docx.text.paragraph import Paragraph
import re
import os

def extract_text_from_docx(docx_path):
    """Extract text from docx file and convert to Markdown."""
    doc = Document(docx_path)

    chapters = []
    current_chapter = None
    current_content = []

    for element in doc.element.body:
        if isinstance(element, CT_P):
            para = Paragraph(element, doc)
            text = para.text.strip()

            if not text:
                # Preserve empty lines
                if current_content:
                    current_content.append("")
                continue

            # Check if this is a heading
            style_name = para.style.name if para.style else ""

            # Check for chapter headings (Heading 1 or lines that start with "Chapter")
            if style_name.startswith('Heading 1') or re.match(r'^(Chapter|CHAPTER)\s+\d+', text):
                # Save previous chapter if exists
                if current_chapter is not None:
                    chapters.append({
                        'title': current_chapter,
                        'content': '\n'.join(current_content)
                    })

                # Start new chapter
                current_chapter = text
                current_content = [f"# {text}\n"]

            elif style_name.startswith('Heading 2'):
                current_content.append(f"\n## {text}\n")
            elif style_name.startswith('Heading 3'):
                current_content.append(f"\n### {text}\n")
            elif style_name.startswith('Heading 4'):
                current_content.append(f"\n#### {text}\n")
            elif style_name.startswith('Heading 5'):
                current_content.append(f"\n##### {text}\n")
            elif style_name.startswith('Heading 6'):
                current_content.append(f"\n###### {text}\n")
            else:
                # Regular paragraph
                # Check for bold, italic formatting
                formatted_text = ""
                for run in para.runs:
                    run_text = run.text
                    if run.bold and run.italic:
                        formatted_text += f"***{run_text}***"
                    elif run.bold:
                        formatted_text += f"**{run_text}**"
                    elif run.italic:
                        formatted_text += f"*{run_text}*"
                    else:
                        formatted_text += run_text

                current_content.append(formatted_text)

        elif isinstance(element, CT_Tbl):
            # Handle tables
            table = Table(element, doc)
            current_content.append("\n")

            # Create markdown table
            for i, row in enumerate(table.rows):
                cells = [cell.text.strip() for cell in row.cells]
                current_content.append("| " + " | ".join(cells) + " |")

                # Add separator after header row
                if i == 0:
                    current_content.append("|" + "|".join(["---" for _ in cells]) + "|")

            current_content.append("\n")

    # Save last chapter
    if current_chapter is not None:
        chapters.append({
            'title': current_chapter,
            'content': '\n'.join(current_content)
        })

    # If no chapters were detected, save everything as a single file
    if not chapters and current_content:
        chapters.append({
            'title': 'Full Document',
            'content': '\n'.join(current_content)
        })

    return chapters

def sanitize_filename(title):
    """Convert chapter title to safe filename."""
    # Remove or replace unsafe characters
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename.lower()

def main():
    docx_path = '/home/user/Translation/ministry.docx'
    output_dir = '/home/user/Translation/chapters'

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract chapters
    chapters = extract_text_from_docx(docx_path)

    print(f"Found {len(chapters)} chapter(s)")

    # Save each chapter to a separate file
    for i, chapter in enumerate(chapters, 1):
        title = chapter['title']
        content = chapter['content']

        # Create filename
        if title == 'Full Document':
            filename = 'full_document.md'
        else:
            safe_title = sanitize_filename(title)
            filename = f"chapter_{i:02d}_{safe_title}.md"

        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Created: {filename}")
        print(f"  Title: {title}")
        print(f"  Length: {len(content)} characters")

if __name__ == '__main__':
    main()
