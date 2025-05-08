from ports import endpoint
from core import endpoints


def connection() -> endpoint.Data:
    return endpoints.MotorolaData
