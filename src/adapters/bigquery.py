from google.cloud import bigquery
from ports import database

class Data(database.Data):
    def getTableSingleRow(table_name: str):
        # Construct a BigQuery client object.
        client = bigquery.Client()

        query = f"""
            SELECT * FROM {table_name} LIMIT 1;
        """
        rows = client.query_and_wait(query)  # Make an API request.

        print("The query data:")
        for row in rows:
            # Row values can be accessed by field name or index.
            print("id={}, member_name={}, icebreaker_joke={}".format(row["id"], row["member_name"], row["icebreaker_joke"]))