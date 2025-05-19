import numpy

from google.cloud import bigquery

from ports import database


class Data(database.Data):
    def get_hay_price_data(self=None):
        rows = request_results()
        return adapt_results(rows)


def request_results():
    client = bigquery.Client()

    query = """
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


def adapt_results(rows):
    normalized_data = {
        row["state_name"].lower().replace(" ", "_"): numpy.median(row["values"])
        for row in rows
    }
    return normalized_data
