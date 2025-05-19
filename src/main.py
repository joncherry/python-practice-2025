import os

from adapters import endpoints
from adapters import sqlite_cache


def main():
    sqlite_cache.create_table()
    if os.environ["LOCAL_RUN_MODE"] == "1":
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    endpoints.app.run("localhost", 8080, debug=True)


if __name__ == "__main__":
    main()
