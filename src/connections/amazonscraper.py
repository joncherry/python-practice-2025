from ports import scraper
from adapters import amazonscraper


def connection() -> scraper.Data:
    return amazonscraper.Data
