import flask

app = flask.Flask(__name__)


def main():
    app.run("localhost", 8080)


if __name__ == "__main__":
    main()
