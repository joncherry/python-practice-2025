from google.cloud import bigquery
from ports import source

class BigQueryData():
    def getTableSingleRow(self, table_name: str):
        # Construct a BigQuery client object.
        client = bigquery.Client()

        query = """
            SELECT name, SUM(number) as total_people
            FROM `bigquery-public-data.usa_names.usa_1910_2013`
            WHERE state = 'TX'
            GROUP BY name, state
            ORDER BY total_people DESC
            LIMIT 20
        """
        rows = client.query_and_wait(query)  # Make an API request.

        print("The query data:")
        for row in rows:
            # Row values can be accessed by field name or index.
            print("name={}, count={}".format(row[0], row["total_people"]))