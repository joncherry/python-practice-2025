import flask

from connections import homehaypriceendpoint
from connections import amazonendpoint
from connections import motorolaendpoint

app = flask.Flask(__name__)


@app.route("/home_and_hay_data", methods=["GET"])
def get_home_and_hay_data():
    home_and_hay_report = homehaypriceendpoint.connection()
    return home_and_hay_report.get_endpoint_report()


@app.route("/amazon_data", methods=["GET"])
def get_amazon_data():
    amazon_report = amazonendpoint.connection()
    return amazon_report.get_endpoint_report()


@app.route("/motorola_data", methods=["GET"])
def get_motorola_data():
    motorola_report = motorolaendpoint.connection()
    return motorola_report.get_endpoint_report()
