#!/usr/bin/env python3
"""
Split large markdown chapter files into smaller subchapter files for easier LLM processing.
Splits based on section headers (## headings) while keeping reasonable file sizes.
"""

import os
import sys
import re
from pathlib import Path


def split_chapter(input_file, output_dir, max_lines_per_chunk=500):
    """
    Split a markdown file into smaller chunks based on section headers.

    Args:
        input_file: Path to the input markdown file
        output_dir: Directory to write subchapter files
        max_lines_per_chunk: Maximum lines per chunk (approximate)
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Get the base name for output files
    input_path = Path(input_file)
    base_name = input_path.stem

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all section headers (## level)
    sections = []
    current_section = {'start': 0, 'title': 'intro', 'lines': []}

    for i, line in enumerate(lines):
        # Check if this is a level 2 header (##)
        if line.strip().startswith('## ') and not line.strip().startswith('### '):
            # Save previous section if it has content
            if current_section['lines']:
                sections.append(current_section)

            # Start new section
            title = line.strip().replace('## ', '').lower()
            title = re.sub(r'[^a-z0-9\s-]', '', title)  # Remove special chars
            title = re.sub(r'\s+', '_', title)  # Replace spaces with underscores
            current_section = {'start': i, 'title': title, 'lines': []}

        current_section['lines'].append(line)

    # Don't forget the last section
    if current_section['lines']:
        sections.append(current_section)

    # If no sections found, treat entire file as one section
    if len(sections) == 1 and sections[0]['title'] == 'intro':
        # Split by line count instead
        return split_by_line_count(lines, base_name, output_dir, max_lines_per_chunk)

    # Write each section to a file, potentially splitting large sections
    chunk_num = 1
    for section in sections:
        section_lines = section['lines']

        # If section is too large, split it further
        if len(section_lines) > max_lines_per_chunk:
            sub_chunks = split_lines_into_chunks(section_lines, max_lines_per_chunk)
            for sub_idx, sub_chunk in enumerate(sub_chunks):
                output_file = os.path.join(output_dir, f"{base_name}_part{chunk_num:02d}.md")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.writelines(sub_chunk)
                print(f"Created: {output_file} ({len(sub_chunk)} lines)")
                chunk_num += 1
        else:
            output_file = os.path.join(output_dir, f"{base_name}_part{chunk_num:02d}.md")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(section_lines)
            print(f"Created: {output_file} ({len(section_lines)} lines)")
            chunk_num += 1

    return chunk_num - 1


def split_by_line_count(lines, base_name, output_dir, max_lines_per_chunk):
    """Split content by line count when no clear sections exist."""
    chunks = split_lines_into_chunks(lines, max_lines_per_chunk)

    for idx, chunk in enumerate(chunks, 1):
        output_file = os.path.join(output_dir, f"{base_name}_part{idx:02d}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(chunk)
        print(f"Created: {output_file} ({len(chunk)} lines)")

    return len(chunks)


def split_lines_into_chunks(lines, max_lines):
    """Split a list of lines into chunks of maximum size."""
    chunks = []
    current_chunk = []

    for line in lines:
        current_chunk.append(line)
        if len(current_chunk) >= max_lines:
            chunks.append(current_chunk)
            current_chunk = []

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def main():
    if len(sys.argv) < 2:
        print("Usage: python split_chapters.py <input_file_or_directory> [output_directory]")
        print("\nExamples:")
        print("  python split_chapters.py English/chapters/chapter_01.md English/subchapters")
        print("  python split_chapters.py English/chapters English/subchapters")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "subchapters"

    # Check if input is a directory or file
    if os.path.isdir(input_path):
        # Process all .md files in directory
        md_files = sorted(Path(input_path).glob("*.md"))
        if not md_files:
            print(f"No .md files found in {input_path}")
            sys.exit(1)

        print(f"Processing {len(md_files)} files from {input_path}...")
        total_chunks = 0
        for md_file in md_files:
            print(f"\n{'='*60}")
            print(f"Processing: {md_file.name}")
            print('='*60)
            chunks = split_chapter(str(md_file), output_dir)
            total_chunks += chunks

        print(f"\n{'='*60}")
        print(f"Total: Created {total_chunks} subchapter files in {output_dir}/")
        print('='*60)
    else:
        # Process single file
        if not os.path.exists(input_path):
            print(f"Error: File not found: {input_path}")
            sys.exit(1)

        chunks = split_chapter(input_path, output_dir)
        print(f"\nCreated {chunks} subchapter files in {output_dir}/")


if __name__ == "__main__":
    main()
