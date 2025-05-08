import nasdaqdatalink
from ports import externalsource
import yaml


class Data(externalsource.Data):
    def get_home_price_data(self=None):
        raw_data = request_home_prices()

        normalized_data = adapt_home_prices(raw_data)

        return normalized_data


def request_home_prices():
    config = yaml.safe_load(open("./config.yaml"))
    statesMap = config["nasdaqStatesMap"]

    states = {
        stateKey: nasdaqdatalink.get_table(
            "ZILLOW/DATA", indicator_id="ZSFH", region_id=statesMap[stateKey]
        )
        for stateKey in statesMap
    }

    return states


def adapt_home_prices(raw_data):
    normalized_data = {
        stateName: raw_data[stateName][raw_data[stateName]["date"].dt.year == 2021][
            ["value"]
        ]
        .median()
        .value
        for stateName in raw_data
    }
    return normalized_data
