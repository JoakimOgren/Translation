#!/usr/bin/env python3
"""
Join translated subchapter files back into complete chapter files.
"""

import os
import sys
import re
from pathlib import Path
from collections import defaultdict


def group_subchapters(subchapter_dir):
    """
    Group subchapter files by their parent chapter.

    Args:
        subchapter_dir: Directory containing subchapter files

    Returns:
        Dictionary mapping chapter names to lists of subchapter files
    """
    md_files = sorted(Path(subchapter_dir).glob("*.md"))

    # Group files by chapter prefix
    chapters = defaultdict(list)

    for md_file in md_files:
        # Extract chapter name from filename
        # E.g., "chapter_01_chapter_1_the_quest_for_fulfillment_part01.md"
        # Should group under "chapter_01_chapter_1_the_quest_for_fulfillment"
        match = re.match(r'(.+?)_part\d+\.md$', md_file.name)
        if match:
            chapter_name = match.group(1)
            chapters[chapter_name].append(md_file)
        else:
            print(f"Warning: Skipping file with unexpected format: {md_file.name}")

    # Sort subchapters within each chapter
    for chapter_name in chapters:
        chapters[chapter_name] = sorted(chapters[chapter_name])

    return chapters


def join_chapter(subchapter_files, output_file):
    """
    Join multiple subchapter files into a single chapter file.

    Args:
        subchapter_files: List of subchapter file paths to join
        output_file: Path to write the joined chapter
    """
    print(f"Joining {len(subchapter_files)} subchapters -> {output_file}")

    # Read and concatenate all subchapter content
    full_content = []

    for i, subchapter_file in enumerate(subchapter_files):
        with open(subchapter_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add content
        full_content.append(content)

        # Add separator between parts (except after last part)
        if i < len(subchapter_files) - 1:
            # Only add newline if content doesn't already end with double newline
            if not content.endswith('\n\n'):
                if content.endswith('\n'):
                    full_content.append('\n')
                else:
                    full_content.append('\n\n')

        print(f"  ✓ Added: {subchapter_file.name}")

    # Write joined content
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(full_content))

    print(f"✓ Created chapter file: {output_file}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python join_subchapters.py <subchapter_dir> <output_dir>")
        print("\nExamples:")
        print("  python join_subchapters.py Swedish/subchapters Swedish/chapters")
        sys.exit(1)

    subchapter_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(subchapter_dir):
        print(f"Error: Subchapter directory not found: {subchapter_dir}")
        sys.exit(1)

    # Group subchapters by chapter
    chapters = group_subchapters(subchapter_dir)

    if not chapters:
        print(f"No subchapter files found in {subchapter_dir}")
        sys.exit(1)

    print(f"Found {len(chapters)} chapters to join")
    print(f"Output directory: {output_dir}")
    print("="*60)

    # Join each chapter
    for chapter_name, subchapter_files in sorted(chapters.items()):
        output_file = os.path.join(output_dir, f"{chapter_name}.md")
        join_chapter(subchapter_files, output_file)
        print()

    print("="*60)
    print(f"Joining complete! Created {len(chapters)} chapter files in {output_dir}/")


if __name__ == "__main__":
    main()
