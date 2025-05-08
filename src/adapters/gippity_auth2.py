# -*- coding: utf-8 -*-

import os
import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"

# Add scopes for Drive, Calendar, and User Info
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
]

USER_INFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"
API_SERVICE_NAME = "drive"
API_VERSION = "v2"

app = flask.Flask(__name__)
app.secret_key = "REPLACE_ME_WITH_A_SECRET_KEY"


@app.route("/")
def index():
    if "user_info" in flask.session:
        user = flask.session["user_info"]
        return (
            f"<p>Signed in as: {user['email']}</p>"
            f"<p>Name: {user['name']}</p>"
            f"<img src='{user['picture']}' alt='User photo'><br>"
            "<a href='/drive'>Drive API</a><br>"
            "<a href='/calendar'>Calendar</a><br>"
            "<a href='/clear'>Logout</a><br>"
        )
    return print_index_table()


@app.route("/drive")
def drive_api_request():
    if "credentials" not in flask.session:
        return flask.redirect("authorize")

    features = flask.session["features"]

    if features.get("drive"):
        credentials = google.oauth2.credentials.Credentials(
            **flask.session["credentials"]
        )

        drive = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials
        )

        files = drive.files().list().execute()

        flask.session["credentials"] = credentials_to_dict(credentials)

        return flask.jsonify(**files)
    else:
        return "<p>Drive feature is not enabled.</p>"


@app.route("/calendar")
def calendar_api_request():
    if "credentials" not in flask.session:
        return flask.redirect("authorize")

    features = flask.session["features"]

    if features.get("calendar"):
        return "<p>User granted the Google Calendar read permission.</p>"
    else:
        return "<p>Calendar feature is not enabled.</p>"


@app.route("/authorize")
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    flask.session["state"] = state
    return flask.redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = flask.session["state"]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    flow.fetch_token(authorization_response=flask.request.url)

    credentials = flow.credentials
    flask.session["credentials"] = credentials_to_dict(credentials)

    # Check which scopes were granted
    features = check_granted_scopes(credentials)
    flask.session["features"] = features

    # Fetch user info to confirm user is signed in
    user_info = requests.get(
        USER_INFO_ENDPOINT, headers={"Authorization": f"Bearer {credentials.token}"}
    ).json()

    flask.session["user_info"] = {
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
    }

    return flask.redirect("/")


@app.route("/revoke")
def revoke():
    if "credentials" not in flask.session:
        return 'You need to <a href="/authorize">authorize</a> before testing the code.'

    credentials = google.oauth2.credentials.Credentials(**flask.session["credentials"])

    revoke = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    if revoke.status_code == 200:
        return "Credentials successfully revoked." + print_index_table()
    else:
        return "An error occurred." + print_index_table()


@app.route("/clear")
def clear_credentials():
    flask.session.clear()
    return "Session cleared.<br><br>" + print_index_table()


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "granted_scopes": credentials.granted_scopes,
    }


def check_granted_scopes(credentials):
    granted = credentials.granted_scopes or []
    return {
        "drive": "https://www.googleapis.com/auth/drive.metadata.readonly" in granted,
        "calendar": "https://www.googleapis.com/auth/calendar.readonly" in granted,
    }


def print_index_table():
    return (
        "<table>"
        + '<tr><td><a href="/authorize">Sign in with Google</a></td>'
        + "<td>Start the OAuth 2.0 authorization flow.</td></tr>"
        + '<tr><td><a href="/drive">Drive API Request</a></td>'
        + "<td>Make a sample request to the Drive API (if scope granted).</td></tr>"
        + '<tr><td><a href="/calendar">Calendar API Check</a></td>'
        + "<td>Check if Calendar scope was granted.</td></tr>"
        + '<tr><td><a href="/revoke">Revoke Credentials</a></td>'
        + "<td>Revoke current access token.</td></tr>"
        + '<tr><td><a href="/clear">Clear Session</a></td>'
        + "<td>Clear credentials and user info from session.</td></tr>"
        + "</table>"
    )


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    app.run("localhost", 8080, debug=True)
