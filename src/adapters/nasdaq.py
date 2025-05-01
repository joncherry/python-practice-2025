import nasdaqdatalink
from ports import externalsource
import yaml

class Data(externalsource.Data):
    def getHomePriceData():
        raw_data = requestHomePrices()

        normalized_data = adaptHomePrices(raw_data)

        return normalized_data

def requestHomePrices():
        config = yaml.safe_load(open("./config.yaml"))
        statesMap = config["nasdaqStatesMap"]
        
        states = {
            stateKey: nasdaqdatalink.get_table('ZILLOW/DATA',indicator_id='ZSFH', region_id=statesMap[stateKey])
            for stateKey in statesMap
        }

        return states

def adaptHomePrices(raw_data):
    normalized_data = {
        stateName: raw_data[stateName][raw_data[stateName]["date"].dt.year == 2021][["value"]].median().value
        for stateName in raw_data
    }
    return normalized_data