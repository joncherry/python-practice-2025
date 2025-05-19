import time
import flask

from connections import homehaypriceendpoint
from connections import amazonendpoint
from connections import motorolaendpoint

from adapters import auth
from adapters import sqlite_cache

app = auth.auth_app


NOT_AUTHORIZED = (
    "please use the /authorize endpoint to sign in before using other endpoints"
)


def auth_wrapper(endpoint_handler):

    def wrapper():
        invalid_result = validate_auth()
        if invalid_result is not None:
            return invalid_result
        return endpoint_handler()

    return wrapper


@app.route("/home_and_hay_data", methods=["GET"])
def get_home_and_hay_handler():
    return get_home_and_hay_data()


@auth_wrapper
def get_home_and_hay_data():
    home_and_hay_report = homehaypriceendpoint.connection()
    return home_and_hay_report.get_endpoint_report()


@app.route("/amazon_data", methods=["GET"])
def get_amazon_handler():
    return get_amazon_data()


@auth_wrapper
def get_amazon_data():
    amazon_report = amazonendpoint.connection()
    return amazon_report.get_endpoint_report()


@app.route("/motorola_data", methods=["GET"])
def get_motorola_handler():
    return get_motorola_data()


@auth_wrapper
def get_motorola_data():
    motorola_report = motorolaendpoint.connection()
    return motorola_report.get_endpoint_report()


def validate_auth():
    session_id = flask.request.headers.get("SESSION-ID")
    if session_id == "":
        return "no session_id given on request headers"
    row = sqlite_cache.read(session_id)
    if row is None or not row:
        return "session ID not found"

    # remove the session after 24 hours
    now = int(time.time())
    older_than_one_day = now - row["unix_time"] > 86400
    if older_than_one_day:
        sqlite_cache.write(
            session_id=session_id,
            unix_time=0,
            credentials={},
            email=False,
            profile=False,
        )
        return "session has expired after 24 hours"

    if not row["email"]:
        return NOT_AUTHORIZED

    if not row["profile"]:
        return NOT_AUTHORIZED
    return None
