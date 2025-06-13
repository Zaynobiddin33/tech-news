from django.core.management.base import BaseCommand
from main.utils import run_news_scraper

class Command(BaseCommand):
    help = "Run daily tech news scraper"

    def handle(self, *args, **kwargs):
        run_news_scraper()
        self.stdout.write(self.style.SUCCESS("✅ News scraping completed"))