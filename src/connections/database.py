from ports import database
from adapters import bigquery


def connection() -> database.Data:
    return bigquery.Data
