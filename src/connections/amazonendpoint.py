from ports import endpointreport
from core import reports


def connection() -> endpointreport.Data:
    return reports.AmazonData
