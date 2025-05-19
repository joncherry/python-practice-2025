import csv
import io

from ports import endpointreport
from connections import externalsource
from connections import database
from connections import amazonscraper
from connections import motorolascraper


class HomeHayPriceData(endpointreport.Data):
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
    with io.StringIO() as csvfile:
        csv_writer = csv.DictWriter(
            csvfile,
            fieldnames=["stateName", "medianHomePrice", "medianHayPrice", "ratio"],
        )
        csv_writer.writeheader()
        csv_writer.writerows(home_and_hay_results)
        return csvfile.getvalue()


class AmazonData(endpointreport.Data):
    def get_endpoint_report(self=None):
        amazon_scraper_data = amazonscraper.connection()
        amazon_results = amazon_scraper_data.get_scrape_result()

        amazon_keys = None
        if len(amazon_results) > 0:
            amazon_keys = amazon_results[0].keys()

        with io.StringIO() as csvfile:
            csv_writer = csv.DictWriter(
                csvfile,
                fieldnames=amazon_keys,
            )
            csv_writer.writeheader()
            csv_writer.writerows(amazon_results)
            return csvfile.getvalue()


class MotorolaData(endpointreport.Data):
    def get_endpoint_report(self=None):
        motorola_scraper_data = motorolascraper.connection()
        motorola_results = motorola_scraper_data.get_scrape_result()

        motorola_keys = None
        if len(motorola_results) > 0:
            motorola_keys = motorola_results[0].keys()

        with io.StringIO() as csvfile:
            csv_writer = csv.DictWriter(
                csvfile,
                fieldnames=motorola_keys,
            )
            csv_writer.writeheader()
            csv_writer.writerows(motorola_results)
            return csvfile.getvalue()
