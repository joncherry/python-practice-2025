from connections import externalsource
from connections import database

def run():
    sourceData = externalsource.connection()
    homePrices = sourceData.getHomePriceData()
    
    databaseData = database.connection()
    hayPrices = databaseData.getHayPriceData()

    ratios = {}
    for state in hayPrices:
        ratios[state] = homePrices[state] / hayPrices[state]
    
    return ratios
    