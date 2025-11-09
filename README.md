# Aftonbladet News Scraper

A Python script to download the top news articles from Aftonbladet (Swedish news site) and save them as Markdown files.

## Features

- Downloads top 10 news articles from Aftonbladet RSS feed
- Extracts article title, preview, and full content
- Saves each article as a formatted Markdown file
- Timestamps each download with publication and download dates
- Includes source URL for reference
- Automatic fallback to demo mode if site is not accessible
- Explicit demo mode for testing

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Normal Mode (Live Articles)

Run the scraper to fetch real articles:

```bash
python aftonbladet_scraper.py
```

This will:
1. Fetch the Aftonbladet RSS feed
2. Extract the top 10 news articles
3. Download the full content of each article
4. Save each article as a Markdown file in the `articles/` directory
5. Automatically fall back to demo mode if the RSS feed is not accessible

### Demo Mode

To test the scraper with sample articles:

```bash
python aftonbladet_scraper.py --demo
# or
python aftonbladet_scraper.py -d
```

This creates 10 sample articles to demonstrate the functionality without accessing the live site.

## Important Notes

### Geo-blocking and Access Restrictions

Aftonbladet may block access from certain geographic locations or detect automated requests. If you encounter a `403 Forbidden` error:

1. **Use a VPN**: Connect to a Swedish VPN server
2. **Run from Sweden**: Execute the script from a Swedish IP address
3. **Demo Mode**: Use `--demo` flag to test the functionality with sample data

The script will automatically fall back to demo mode if it cannot access the RSS feed.

## Output

Articles are saved in the `articles/` directory with filenames in the format:
```
YYYY-MM-DD_article_title.md
```

Each Markdown file contains:
- Article title
- Download date/time
- Source URL
- Article summary/preview
- Full article content

## Example

```bash
$ python aftonbladet_scraper.py
Fetching top 10 articles from Aftonbladet...
Found 10 articles

[1/10] Processing: Breaking news headline...
✓ Saved: 2025-11-09_breaking_news_headline.md

[2/10] Processing: Another important story...
✓ Saved: 2025-11-09_another_important_story.md

...

✓ Successfully downloaded 10 articles to './articles/' directory
```

## Requirements

- Python 3.6+
- requests
- beautifulsoup4

## Notes

- The scraper includes a 1-second delay between requests to be polite to the server
- Uses proper User-Agent headers to simulate a regular browser
- Handles various article formats from Aftonbladet's different sections (news, sports, entertainment)
