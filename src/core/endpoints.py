from ports import endpoint
from connections import externalsource
from connections import database
from connections import amazonscraper
from connections import motorolascraper


class HomeHayPriceData(endpoint.Data):
    def get_endpoint_report(self=None):
        source_data = externalsource.connection()
        home_prices = source_data.get_home_price_data()

        database_data = database.connection()
        hay_prices = database_data.get_hay_price_data()

        home_and_hay_results = calculationsOnHomeAndHay(home_prices, hay_prices)

        return home_and_hay_results


def calculationsOnHomeAndHay(home_prices, hay_prices):
    home_and_hay_results = []
    for state in hay_prices:
        home_and_hay_results.append(
            {
                "stateName": state,
                "medianHomePrice": home_prices[state],
                "medianHayPrice": hay_prices[state],
                "ratio": home_prices[state] / hay_prices[state],
            }
        )
    return home_and_hay_results


class AmazonData(endpoint.Data):
    def get_endpoint_report(self=None):
        amazon_scraper_data = amazonscraper.connection()
        amazon_results = amazon_scraper_data.get_scrape_result()
        return amazon_results


class MotorolaData(endpoint.Data):
    def get_endpoint_report(self=None):
        motorola_scraper_data = motorolascraper.connection()
        motorola_results = motorola_scraper_data.get_scrape_result()
        return motorola_results
