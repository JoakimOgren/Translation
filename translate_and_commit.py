#!/usr/bin/env python3
"""
Translate markdown subchapter files from English to Swedish and commit each one.
"""

import os
import sys
import subprocess
from pathlib import Path
import anthropic


def run_git_command(command):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e.stderr}")
        return None


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


def translate_and_commit_file(input_file, output_file, api_key):
    """
    Translate a single markdown file and commit it.

    Args:
        input_file: Path to English markdown file
        output_file: Path to write Swedish translation
        api_key: Anthropic API key
    """
    filename = os.path.basename(input_file)
    print(f"\n[{filename}] Starting translation...")

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

        print(f"[{filename}] ✓ Translated ({len(english_content)} -> {len(swedish_content)} chars)")

        # Git add and commit
        run_git_command(f"git add {output_file}")
        commit_msg = f"Add Swedish translation: {os.path.basename(output_file)}"
        run_git_command(f'git commit -m "{commit_msg}"')
        print(f"[{filename}] ✓ Committed")

        return True
    except Exception as e:
        print(f"[{filename}] ✗ Error: {str(e)}")
        return False


def main():
    input_dir = "English/subchapters"
    output_dir = "Swedish/subchapters"
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
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
    print("="*60)

    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, md_file in enumerate(md_files, 1):
        output_file = os.path.join(output_dir, md_file.name)

        # Skip if already translated
        if os.path.exists(output_file):
            print(f"\n[{i}/{len(md_files)}] ⊘ Skipping (already exists): {md_file.name}")
            skip_count += 1
            continue

        print(f"\n[{i}/{len(md_files)}] Processing: {md_file.name}")

        if translate_and_commit_file(str(md_file), output_file, api_key):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "="*60)
    print(f"Translation complete!")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {fail_count}")
    print(f"  Skipped: {skip_count}")
    print(f"  Total: {len(md_files)}")


if __name__ == "__main__":
    main()
