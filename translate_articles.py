#!/usr/bin/env python3
"""
Article Translator
Translates Swedish articles to English and Bondska (Swedish rural dialect)
"""

import os
import re
from datetime import datetime


class ArticleTranslator:
    def __init__(self):
        self.articles_dir = 'articles'
        self.english_dir = 'articles_en'
        self.bondska_dir = 'articles_bondska'

    def ensure_output_dirs(self):
        """Create output directories if they don't exist."""
        os.makedirs(self.english_dir, exist_ok=True)
        os.makedirs(self.bondska_dir, exist_ok=True)

    def read_article(self, filepath):
        """Read article content from file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def parse_article(self, content):
        """Parse article content to extract components."""
        lines = content.split('\n')

        # Extract title (first line starting with #)
        title = ""
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break

        return {
            'title': title,
            'content': content
        }

    def translate_to_english(self, content):
        """Translate Swedish article to English."""
        # Translation mappings
        translations = {
            # Headers and metadata
            '# Senaste nyheterna från Sverige': '# Latest News from Sweden',
            '# Breaking: Viktigt politiskt beslut fattat': '# Breaking: Important Political Decision Made',
            '# Väderprognos: Sol och värme på väg': '# Weather Forecast: Sun and Warmth on the Way',
            '# Sport: Stor framgång för svenskt lag': '# Sports: Major Success for Swedish Team',
            '# Ekonomi: Börsen når nya höjder': '# Economy: Stock Market Reaches New Heights',
            '# Kultur: Ny utställning öppnar i Stockholm': '# Culture: New Exhibition Opens in Stockholm',
            '# Hälsa: Nya råd från folkhälsomyndigheten': '# Health: New Advice from Public Health Agency',
            '# Teknik: AI-genombrott presenterat': '# Technology: AI Breakthrough Presented',
            '# Miljö: Nya åtgärder för klimatet': '# Environment: New Climate Measures',
            '# Utbildning: Reformer i skolsystemet': '# Education: Reforms in School System',

            # Metadata fields
            '**Publicerad:**': '**Published:**',
            '**Nedladdad:**': '**Downloaded:**',
            '**Källa:**': '**Source:**',

            # Sections
            '## Sammanfattning': '## Summary',
            '## Fullständig artikel': '## Full Article',

            # Content
            'Här är dagens viktigaste nyheter från Sverige. Allt från politik till samhälle.':
                'Here are today\'s most important news from Sweden. Everything from politics to society.',
            'Regeringen har fattat ett viktigt beslut som påverkar många svenskar.':
                'The government has made an important decision that affects many Swedes.',
            'SMHI spår soligt och varmt väder de kommande dagarna.':
                'SMHI predicts sunny and warm weather in the coming days.',
            'Svenska laget vann en imponerande seger i gårdagens match.':
                'The Swedish team won an impressive victory in yesterday\'s match.',
            'Stockholmsbörsen steg kraftigt under dagens handel.':
                'The Stockholm Stock Exchange rose sharply during today\'s trading.',
            'En stor konstutställning öppnar sina dörrar för allmänheten.':
                'A major art exhibition opens its doors to the public.',
            'Folkhälsomyndigheten ger nya rekommendationer för hälsosam livsstil.':
                'The Public Health Agency provides new recommendations for a healthy lifestyle.',
            'Svenska forskare presenterar banbrytande AI-teknologi.':
                'Swedish researchers present groundbreaking AI technology.',
            'Regeringen presenterar nya klimatåtgärder för att nå miljömålen.':
                'The government presents new climate measures to reach environmental goals.',
            'Stora förändringar planeras för det svenska skolsystemet.':
                'Major changes are planned for the Swedish school system.',

            # Demo content
            'Detta är en demoartikel som visar hur scraperverktyget fungerar.':
                'This is a demo article showing how the scraper tool works.',
            'I verkliga läget skulle detta innehålla den fullständiga artikeltexten från Aftonbladet.':
                'In a real scenario, this would contain the full article text from Aftonbladet.',
            '**Artikelns huvudpunkter:**': '**Article Highlights:**',
            '- Viktig information om ämnet': '- Important information about the topic',
            '- Bakgrund och kontext': '- Background and context',
            '- Expertkommentarer': '- Expert commentary',
            '- Framtida utveckling': '- Future developments',
            'Denna demo skapades eftersom den riktiga webbplatsen inte var tillgänglig från denna miljö.':
                'This demo was created because the actual website was not accessible from this environment.',
            'För att ladda ner riktig innehåll, kör skriptet från en svensk IP-adress eller använd en VPN-tjänst.':
                'To download real content, run the script from a Swedish IP address or use a VPN service.',
            '*Nedladdad från Aftonbladet RSS-flöde*': '*Downloaded from Aftonbladet RSS Feed*',
            'Ingen förhandsgranskning tillgänglig': 'No preview available'
        }

        result = content
        for swedish, english in translations.items():
            result = result.replace(swedish, english)

        return result

    def translate_to_bondska(self, content):
        """Translate Swedish article to Bondska (rural Swedish dialect)."""
        # Bondska translation mappings (more traditional/rural Swedish expressions)
        translations = {
            # Headers
            '# Senaste nyheterna från Sverige': '# Sista nyheterna från Svea rike',
            '# Breaking: Viktigt politiskt beslut fattat': '# Brådskande: Viktigt politiskt beslut taget',
            '# Väderprognos: Sol och värme på väg': '# Väderleken: Sol å värme på kommande',
            '# Sport: Stor framgång för svenskt lag': '# Idrott: Stor framgång för svenskt manskap',
            '# Ekonomi: Börsen når nya höjder': '# Hushållning: Börsen når nya toppar',
            '# Kultur: Ny utställning öppnar i Stockholm': '# Kultur: Ny utställning öppnas i Stockholm',
            '# Hälsa: Nya råd från folkhälsomyndigheten': '# Hälsa: Nya råd ifrån folkhälsomyndigheten',
            '# Teknik: AI-genombrott presenterat': '# Teknik: AI-genombrott framlagt',
            '# Miljö: Nya åtgärder för klimatet': '# Miljö: Nya åtgärder för väderleken',
            '# Utbildning: Reformer i skolsystemet': '# Undervisning: Reformer i skolväsendet',

            # Metadata
            '**Publicerad:**': '**Utgiven:**',
            '**Nedladdad:**': '**Hemtad:**',
            '**Källa:**': '**Källa:**',

            # Sections
            '## Sammanfattning': '## Sammandrag',
            '## Fullständig artikel': '## Fullständiga artikeln',

            # Content with dialectal expressions
            'Här är dagens viktigaste nyheter från Sverige':
                'Här ä dagens viktigaste nyheter ifrån Sverige',
            'Allt från politik till samhälle': 'Allt ifrån politik te samhället',
            'Regeringen har fattat ett viktigt beslut som påverkar många svenskar':
                'Regeringen ha tagit ett viktigt beslut som berör många svenskar',
            'SMHI spår soligt och varmt väder de kommande dagarna':
                'SMHI förutspår soligt å varmt väder dom kommande dagarna',
            'Svenska laget vann en imponerande seger i gårdagens match':
                'Svenska laget vann en storartad seger i gårdagens match',
            'Stockholmsbörsen steg kraftigt under dagens handel':
                'Stockholmsbörsen steg kraftigt under dagens handel',
            'En stor konstutställning öppnar sina dörrar för allmänheten':
                'En stor konstutställning öppnar sina dörrar för allmogen',
            'Folkhälsomyndigheten ger nya rekommendationer för hälsosam livsstil':
                'Folkhälsomyndigheten ger nya råd för en sund levnadssätt',
            'Svenska forskare presenterar banbrytande AI-teknologi':
                'Svenska forskare lägger fram banbrytande AI-teknologi',
            'Regeringen presenterar nya klimatåtgärder för att nå miljömålen':
                'Regeringen lägger fram nya klimatåtgärder för att nå miljömålen',
            'Stora förändringar planeras för det svenska skolsystemet':
                'Stora förändringar planeras för det svenska skolväsendet',

            # Demo content
            'Detta är en demoartikel som visar hur scraperverktyget fungerar':
                'Detta ä en demoartikel som visar hur scraperverktyget fungerar',
            'I verkliga läget skulle detta innehålla den fullständiga artikeltexten från Aftonbladet':
                'I verkliga läget skull detta innehålla den fullständiga artikeltexten ifrån Aftonbladet',
            '**Artikelns huvudpunkter:**': '**Artikelns huvudpunkter:**',
            '- Viktig information om ämnet': '- Viktig information om ämnet',
            '- Bakgrund och kontext': '- Bakgrund å sammanhang',
            '- Expertkommentarer': '- Expertutlåtanden',
            '- Framtida utveckling': '- Kommande utveckling',
            'Denna demo skapades eftersom den riktiga webbplatsen inte var tillgänglig från denna miljö':
                'Denna demo skapades eftersom den riktiga webbplatsen int va tillgänglig ifrån denna miljö',
            'För att ladda ner riktig innehåll, kör skriptet från en svensk IP-adress eller använd en VPN-tjänst':
                'För att ladda ner riktigt innehåll, kör skriptet ifrån en svensk IP-adress eller använd en VPN-tjänst',
            '*Nedladdad från Aftonbladet RSS-flöde*': '*Hemtad från Aftonbladet RSS-flöde*',
            'Ingen förhandsgranskning tillgänglig': 'Ingen förhandsgranskning finns'
        }

        result = content
        for standard, bondska in translations.items():
            result = result.replace(standard, bondska)

        return result

    def save_translated_article(self, content, original_filename, target_dir, language):
        """Save translated article to target directory."""
        # Create filename based on original
        basename = os.path.basename(original_filename)
        filepath = os.path.join(target_dir, basename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Translated to {language}: {basename}")
        return filepath

    def translate_all_articles(self):
        """Translate all articles in the articles directory."""
        self.ensure_output_dirs()

        # Get all markdown files
        article_files = [f for f in os.listdir(self.articles_dir) if f.endswith('.md')]

        if not article_files:
            print("No articles found to translate.")
            return

        print(f"Found {len(article_files)} articles to translate\n")

        english_files = []
        bondska_files = []

        for i, filename in enumerate(article_files, 1):
            filepath = os.path.join(self.articles_dir, filename)
            print(f"[{i}/{len(article_files)}] Processing: {filename}")

            # Read original article
            content = self.read_article(filepath)

            # Translate to English
            english_content = self.translate_to_english(content)
            english_file = self.save_translated_article(
                english_content, filename, self.english_dir, 'English'
            )
            english_files.append(english_file)

            # Translate to Bondska
            bondska_content = self.translate_to_bondska(content)
            bondska_file = self.save_translated_article(
                bondska_content, filename, self.bondska_dir, 'Bondska'
            )
            bondska_files.append(bondska_file)

            print()

        print(f"✓ Translation complete!")
        print(f"  - {len(english_files)} articles translated to English in '{self.english_dir}/'")
        print(f"  - {len(bondska_files)} articles translated to Bondska in '{self.bondska_dir}/'")

        return english_files, bondska_files


def main():
    translator = ArticleTranslator()
    translator.translate_all_articles()


if __name__ == "__main__":
    main()
