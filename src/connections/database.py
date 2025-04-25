from ports import database
from adapters import bigquery

def connection() -> database.DatabaseData:
    return bigquery.BigQueryData