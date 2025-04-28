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

        states = {}
        for stateKey in statesMap:
            regionID = statesMap[stateKey]
            states[stateKey] = nasdaqdatalink.get_table('ZILLOW/DATA',indicator_id='ZSFH', region_id=regionID)

        return states

def adaptHomePrices(raw_data):
    normalized_data = {}
    for stateName in raw_data:
        state = raw_data[stateName]
        normalized_data[stateName] = state[state["date"].dt.year == 2021][["value"]].median().value
    return normalized_data