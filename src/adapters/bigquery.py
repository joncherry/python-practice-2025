from google.cloud import bigquery
from ports import database
import numpy

class Data(database.Data):
    def getHayPriceData():
        rows = requestResults()
        return adaptResults(rows)
        
def requestResults():
    client = bigquery.Client()

    query = f"""
        SELECT
            state_name,
            ARRAY_AGG(value) as values
        FROM
            `bigquery-public-data.usda_nass_agriculture.crops`
        WHERE
            commodity_desc = "HAY"
        AND year = 2021
        AND country_name ="UNITED STATES"
        AND unit_desc = "$ / TON"
        AND state_name != "US TOTAL"
        AND state_name is not null
        AND value is not null
        GROUP BY 
            state_name
        LIMIT
            55;
    """
    rows = client.query_and_wait(query)
    return rows

def adaptResults(rows):
    normalized_data = {
        row["state_name"].lower().replace(" ", "_"): numpy.median(row["values"])
        for row in rows
    }
    return normalized_data