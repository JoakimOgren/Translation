#!/bin/bash
#
# Complete Translation Workflow
# This script runs the full translation pipeline from English to Swedish
#

set -e  # Exit on error

echo "=================================================="
echo "Swedish Translation Workflow"
echo "=================================================="
echo

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable is not set"
    echo
    echo "Please set your API key:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo
    echo "Or run with:"
    echo "  ANTHROPIC_API_KEY='your-key' ./run_translation.sh"
    echo
    exit 1
fi

echo "✓ API key found"
echo

# Step 1: Split chapters (already done, but can re-run)
echo "Step 1: Splitting English chapters into subchapters..."
echo "--------------------------------------------------"
python3 split_chapters.py English/chapters English/subchapters
echo
echo "✓ Step 1 complete"
echo

# Step 2: Translate subchapters
echo "Step 2: Translating subchapters to Swedish..."
echo "--------------------------------------------------"
python3 translate_subchapters.py English/subchapters Swedish/subchapters
echo
echo "✓ Step 2 complete"
echo

# Step 3: Join Swedish subchapters
echo "Step 3: Joining Swedish subchapters into chapters..."
echo "--------------------------------------------------"
python3 join_subchapters.py Swedish/subchapters Swedish/chapters
echo
echo "✓ Step 3 complete"
echo

echo "=================================================="
echo "Translation workflow complete!"
echo "=================================================="
echo
echo "Swedish chapters are now available in: Swedish/chapters/"
echo
ls -lh Swedish/chapters/ | tail -n +2
echo
