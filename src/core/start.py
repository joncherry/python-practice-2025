from connections import externalsource
from connections import database
from connections import amazonscraper
from connections import motorolascraper
import csv

def run():
    sourceData = externalsource.connection()
    homePrices = sourceData.getHomePriceData()
    
    databaseData = database.connection()
    hayPrices = databaseData.getHayPriceData()

    homeAndHayResults = []
    for state in hayPrices:
        homeAndHayResults.append({
            "stateName": state,
            "medianHomePrice": homePrices[state],
            "medianHayPrice": hayPrices[state],
            "ratio": homePrices[state] / hayPrices[state],
        })

    amazonScraperData = amazonscraper.connection()
    amazonResults = amazonScraperData.getScrapeResult()
    
    motorolaScraperData = motorolascraper.connection()
    motorolaResults = motorolaScraperData.getScrapeResult()

    

    with open('homeAndHayResults.csv', 'w', newline='') as csvfile:
        fieldnames = ['stateName', 'medianHomePrice', 'medianHayPrice', 'ratio']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in homeAndHayResults:
            writer.writerow(result)

    with open('amazonResults.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'starRating', 'ratingsCount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in amazonResults:
            writer.writerow(result)

    with open('motorolaResults.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'price', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in motorolaResults:
            writer.writerow(result)
    