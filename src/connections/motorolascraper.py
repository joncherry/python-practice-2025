from ports import scraper
from adapters import motorolascraper

def connection() -> scraper.Data:
    return motorolascraper.Data