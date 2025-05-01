from connections import externalsource
from connections import database
from connections import amazonscraper
from connections import motorolascraper
import csv


def run():
    source_data = externalsource.connection()
    home_prices = source_data.get_home_price_data()

    database_data = database.connection()
    hay_prices = database_data.get_hay_price_data()

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

    amazon_scraper_data = amazonscraper.connection()
    amazon_results = amazon_scraper_data.get_scrape_result()

    motorola_scraper_data = motorolascraper.connection()
    motorola_results = motorola_scraper_data.get_scrape_result()

    with open("home_and_hay_results.csv", "w", newline="") as csvfile:
        fieldnames = ["stateName", "medianHomePrice", "medianHayPrice", "ratio"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in home_and_hay_results:
            writer.writerow(result)

    with open("amazon_results.csv", "w", newline="") as csvfile:
        fieldnames = ["title", "starRating", "ratingsCount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in amazon_results:
            writer.writerow(result)

    with open("motorola_results.csv", "w", newline="") as csvfile:
        fieldnames = ["title", "price", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in motorola_results:
            writer.writerow(result)
