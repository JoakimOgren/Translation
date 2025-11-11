#!/usr/bin/env python3
"""
Translate markdown subchapter files from English to Swedish using Claude API.
"""

import os
import sys
import time
from pathlib import Path
import anthropic


def translate_to_swedish(content, api_key):
    """
    Translate English markdown content to Swedish using Claude API.

    Args:
        content: English markdown text to translate
        api_key: Anthropic API key

    Returns:
        Translated Swedish text
    """
    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Please translate the following English text to Swedish. This is a religious/spiritual text about Christian ministry and fulfillment.

IMPORTANT INSTRUCTIONS:
1. Maintain all markdown formatting (headers, bold, italic, lists, etc.)
2. Keep the same paragraph structure
3. Preserve any special formatting or emphasis
4. Translate naturally and idiomatically into Swedish, not word-for-word
5. Keep proper names in their original form
6. Maintain the tone and style of the original text
7. Only output the translated text, no explanations or comments

English text to translate:

{content}"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def translate_file(input_file, output_file, api_key, delay=1):
    """
    Translate a single markdown file from English to Swedish.

    Args:
        input_file: Path to English markdown file
        output_file: Path to write Swedish translation
        api_key: Anthropic API key
        delay: Seconds to wait between API calls (rate limiting)
    """
    print(f"Translating: {input_file} -> {output_file}")

    # Read English content
    with open(input_file, 'r', encoding='utf-8') as f:
        english_content = f.read()

    # Translate to Swedish
    try:
        swedish_content = translate_to_swedish(english_content, api_key)

        # Write Swedish content
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(swedish_content)

        print(f"✓ Successfully translated ({len(english_content)} -> {len(swedish_content)} chars)")

        # Rate limiting
        if delay > 0:
            time.sleep(delay)

        return True
    except Exception as e:
        print(f"✗ Error translating {input_file}: {str(e)}")
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python translate_subchapters.py <input_dir> <output_dir> [api_key]")
        print("\nExamples:")
        print("  python translate_subchapters.py English/subchapters Swedish/subchapters")
        print("  python translate_subchapters.py English/subchapters Swedish/subchapters sk-ant-...")
        print("\nNote: If api_key is not provided, will look for ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    api_key = sys.argv[3] if len(sys.argv) > 3 else os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        print("Error: No API key provided. Set ANTHROPIC_API_KEY environment variable or pass as argument.")
        sys.exit(1)

    if not os.path.isdir(input_dir):
        print(f"Error: Input directory not found: {input_dir}")
        sys.exit(1)

    # Get all markdown files
    md_files = sorted(Path(input_dir).glob("*.md"))
    if not md_files:
        print(f"No .md files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(md_files)} files to translate")
    print(f"Output directory: {output_dir}")
    print("="*60)

    success_count = 0
    fail_count = 0

    for md_file in md_files:
        output_file = os.path.join(output_dir, md_file.name)

        # Skip if already translated
        if os.path.exists(output_file):
            print(f"⊘ Skipping (already exists): {md_file.name}")
            continue

        if translate_file(str(md_file), output_file, api_key):
            success_count += 1
        else:
            fail_count += 1

    print("="*60)
    print(f"Translation complete!")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {fail_count}")
    print(f"  Total: {len(md_files)}")


if __name__ == "__main__":
    main()
