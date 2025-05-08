import flask

app = flask.Flask(__name__)


@app.route("/home_and_hay_data", methods=["GET"])
def get_home_and_hay_data():
    if "credentials" not in flask.session:
        return flask.redirect("authorize")


@app.route("/amazon_data", methods=["GET"])
def get_amazon_data():
    if "credentials" not in flask.session:
        return flask.redirect("authorize")


@app.route("/motorola_data", methods=["GET"])
def get_motorola_data():
    if "credentials" not in flask.session:
        return flask.redirect("authorize")
