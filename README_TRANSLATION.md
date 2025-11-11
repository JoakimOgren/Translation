# Swedish Translation Workflow

This repository contains tools to translate large markdown documents into Swedish by splitting them into manageable chunks.

## Tools Created

### 1. `split_chapters.py`
Splits large markdown chapter files into smaller subchapter files.

**Usage:**
```bash
python3 split_chapters.py <input_dir> <output_dir>
```

**Example:**
```bash
python3 split_chapters.py English/chapters English/subchapters
```

### 2. `translate_subchapters.py`
Translates English subchapter files to Swedish using Claude API.

**Usage:**
```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run translation
python3 translate_subchapters.py English/subchapters Swedish/subchapters
```

**Or pass API key as argument:**
```bash
python3 translate_subchapters.py English/subchapters Swedish/subchapters sk-ant-your-key
```

**Features:**
- Automatically skips already-translated files
- Maintains markdown formatting
- Includes rate limiting to avoid API throttling
- Shows progress for each file

### 3. `join_subchapters.py`
Joins translated subchapter files back into complete chapter files.

**Usage:**
```bash
python3 join_subchapters.py Swedish/subchapters Swedish/chapters
```

## Complete Workflow

### Step 1: Split English Chapters (✓ COMPLETED)
```bash
python3 split_chapters.py English/chapters English/subchapters
```
**Result:** Created 149 subchapter files from 21 chapters

### Step 2: Translate to Swedish (READY TO RUN)
```bash
# Install required package
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Run translation
python3 translate_subchapters.py English/subchapters Swedish/subchapters
```

**Note:** This step requires an Anthropic API key. The translation uses Claude Sonnet 4.5 for high-quality results.

### Step 3: Join Swedish Subchapters
```bash
python3 join_subchapters.py Swedish/subchapters Swedish/chapters
```

## Directory Structure

```
Translation/
├── English/
│   ├── chapters/          # Original full chapter files
│   └── subchapters/       # Split English subchapters (149 files)
├── Swedish/
│   ├── subchapters/       # Translated Swedish subchapters
│   └── chapters/          # Final joined Swedish chapters
├── split_chapters.py      # Tool 1: Split chapters
├── translate_subchapters.py  # Tool 2: Translate
└── join_subchapters.py    # Tool 3: Join subchapters
```

## Translation Progress

- ✅ Step 1: English chapters split into 149 subchapters
- ⏳ Step 2: Translation to Swedish (requires API key)
- ⏳ Step 3: Join Swedish subchapters into chapters

## Cost Estimation

With 149 subchapter files averaging ~300-400 tokens each, the total translation cost should be reasonable. Claude Sonnet 4.5 pricing:
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

Estimated total cost: $5-15 depending on file sizes.
