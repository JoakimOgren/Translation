#!/usr/bin/env python3
"""
Aftonbladet News Scraper
Downloads the top news articles from Aftonbladet and saves them as Markdown files.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import time
import xml.etree.ElementTree as ET


class AftonbladetScraper:
    def __init__(self):
        self.base_url = "https://www.aftonbladet.se"
        self.rss_url = "https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch_rss_feed(self):
        """Fetch the Aftonbladet RSS feed."""
        try:
            response = self.session.get(self.rss_url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching RSS feed: {e}")
            return None

    def parse_rss_feed(self, rss_content, limit=10):
        """Parse RSS feed and extract article information."""
        try:
            root = ET.fromstring(rss_content)
            articles = []

            # Find all item elements in the RSS feed
            for item in root.findall('.//item')[:limit]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                description_elem = item.find('description')
                pubDate_elem = item.find('pubDate')

                if title_elem is not None and link_elem is not None:
                    article = {
                        'title': title_elem.text or '',
                        'url': link_elem.text or '',
                        'preview': description_elem.text if description_elem is not None else '',
                        'pubDate': pubDate_elem.text if pubDate_elem is not None else ''
                    }
                    articles.append(article)

            return articles
        except ET.ParseError as e:
            print(f"Error parsing RSS feed: {e}")
            return []


    def fetch_article_content(self, url):
        """Fetch the full content of an article."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract article content
            content_parts = []

            # Try to find the article body
            article_body = soup.find('article') or soup.find('div', class_=re.compile(r'article|content|body'))

            if article_body:
                # Extract all paragraphs
                paragraphs = article_body.find_all(['p', 'h2', 'h3'])
                for para in paragraphs:
                    text = para.get_text(strip=True)
                    if text and len(text) > 20:  # Filter out short strings
                        if para.name in ['h2', 'h3']:
                            content_parts.append(f"\n## {text}\n")
                        else:
                            content_parts.append(text)

            return '\n\n'.join(content_parts) if content_parts else "Content not available"

        except requests.RequestException as e:
            print(f"Error fetching article {url}: {e}")
            return "Content not available"

    def sanitize_filename(self, title):
        """Create a safe filename from article title."""
        # Remove special characters
        filename = re.sub(r'[^\w\s-]', '', title)
        # Replace spaces with underscores
        filename = re.sub(r'[-\s]+', '_', filename)
        # Limit length
        filename = filename[:100]
        return filename.lower()

    def save_article_as_markdown(self, article, content, output_dir='articles'):
        """Save article as a Markdown file."""
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d')
        filename = f"{timestamp}_{self.sanitize_filename(article['title'])}.md"
        filepath = os.path.join(output_dir, filename)

        # Clean preview text (remove HTML tags if present)
        preview = article.get('preview', '')
        if preview:
            preview_soup = BeautifulSoup(preview, 'html.parser')
            preview = preview_soup.get_text(strip=True)

        pub_date = article.get('pubDate', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        markdown_content = f"""# {article['title']}

**Published:** {pub_date}
**Downloaded:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source:** [Aftonbladet]({article['url']})

---

## Summary

{preview if preview else 'No preview available'}

---

## Full Article

{content}

---

*Downloaded from Aftonbladet RSS Feed*
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"✓ Saved: {filename}")
        return filepath

    def create_demo_articles(self, limit=10):
        """Create demo articles for testing when live site is not accessible."""
        print("⚠ Live site not accessible. Creating demo articles...")

        demo_articles = [
            {
                'title': 'Senaste nyheterna från Sverige',
                'url': 'https://www.aftonbladet.se/nyheter/demo1',
                'preview': 'Här är dagens viktigaste nyheter från Sverige. Allt från politik till samhälle.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Breaking: Viktigt politiskt beslut fattat',
                'url': 'https://www.aftonbladet.se/nyheter/demo2',
                'preview': 'Regeringen har fattat ett viktigt beslut som påverkar många svenskar.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Väderprognos: Sol och värme på väg',
                'url': 'https://www.aftonbladet.se/nyheter/demo3',
                'preview': 'SMHI spår soligt och varmt väder de kommande dagarna.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Sport: Stor framgång för svenskt lag',
                'url': 'https://www.aftonbladet.se/sportbladet/demo4',
                'preview': 'Svenska laget vann en imponerande seger i gårdagens match.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Ekonomi: Börsen når nya höjder',
                'url': 'https://www.aftonbladet.se/nyheter/demo5',
                'preview': 'Stockholmsbörsen steg kraftigt under dagens handel.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Kultur: Ny utställning öppnar i Stockholm',
                'url': 'https://www.aftonbladet.se/nojesbladet/demo6',
                'preview': 'En stor konstutställning öppnar sina dörrar för allmänheten.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Hälsa: Nya råd från folkhälsomyndigheten',
                'url': 'https://www.aftonbladet.se/nyheter/demo7',
                'preview': 'Folkhälsomyndigheten ger nya rekommendationer för hälsosam livsstil.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Teknik: AI-genombrott presenterat',
                'url': 'https://www.aftonbladet.se/nyheter/demo8',
                'preview': 'Svenska forskare presenterar banbrytande AI-teknologi.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Miljö: Nya åtgärder för klimatet',
                'url': 'https://www.aftonbladet.se/nyheter/demo9',
                'preview': 'Regeringen presenterar nya klimatåtgärder för att nå miljömålen.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            },
            {
                'title': 'Utbildning: Reformer i skolsystemet',
                'url': 'https://www.aftonbladet.se/nyheter/demo10',
                'preview': 'Stora förändringar planeras för det svenska skolsystemet.',
                'pubDate': datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
            }
        ]

        return demo_articles[:limit]

    def scrape_top_articles(self, limit=10, demo_mode=False):
        """Main method to scrape top articles and save as Markdown."""

        if demo_mode:
            print(f"Running in DEMO mode - creating {limit} sample articles...")
            articles = self.create_demo_articles(limit)
        else:
            print(f"Fetching top {limit} articles from Aftonbladet RSS feed...")

            # Fetch RSS feed
            rss_content = self.fetch_rss_feed()
            if not rss_content:
                print("\n⚠ Failed to fetch RSS feed.")
                print("This might be due to geo-blocking or network restrictions.")
                print("Falling back to DEMO mode...\n")
                articles = self.create_demo_articles(limit)
            else:
                # Parse RSS feed
                articles = self.parse_rss_feed(rss_content, limit)
                if not articles:
                    print("No articles found in RSS feed. Using demo mode.")
                    articles = self.create_demo_articles(limit)

        print(f"Processing {len(articles)} articles...")

        # Fetch and save each article
        saved_files = []
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] Processing: {article['title'][:60]}...")

            # For demo articles, create demo content
            if 'demo' in article['url']:
                content = f"""Detta är en demoartikel som visar hur scraperverktyget fungerar.

I verkliga läget skulle detta innehålla den fullständiga artikeltexten från Aftonbladet.

**Artikelns huvudpunkter:**

- Viktig information om ämnet
- Bakgrund och kontext
- Expertkommentarer
- Framtida utveckling

Denna demo skapades eftersom den riktiga webbplatsen inte var tillgänglig från denna miljö.
För att ladda ner riktig innehåll, kör skriptet från en svensk IP-adress eller använd en VPN-tjänst.
"""
            else:
                # Fetch full content for real articles
                content = self.fetch_article_content(article['url'])

            # Save as Markdown
            filepath = self.save_article_as_markdown(article, content)
            saved_files.append(filepath)

            # Small delay for demo mode too
            if not demo_mode:
                time.sleep(1)

        print(f"\n✓ Successfully saved {len(saved_files)} articles to './articles/' directory")
        return saved_files


def main():
    import sys

    # Check for demo mode flag
    demo_mode = '--demo' in sys.argv or '-d' in sys.argv

    scraper = AftonbladetScraper()
    scraper.scrape_top_articles(limit=10, demo_mode=demo_mode)


if __name__ == "__main__":
    main()
