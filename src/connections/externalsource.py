from ports import externalsource
from adapters import nasdaq


def connection() -> externalsource.Data:
    return nasdaq.Data
