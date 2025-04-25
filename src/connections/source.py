from ports import source
from adapters import nasdaq

def connection() -> source.SourceData:
    return nasdaq.NasdaqData