import nasdaqdatalink
from ports import source

class NasdaqData(source.SourceData):

    def getHomePriceData():
        idaho = nasdaqdatalink.get_table('ZILLOW/DATA',indicator_id='ZSFH', region_id='20')

        return idaho