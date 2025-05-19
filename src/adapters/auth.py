import webbrowser
import time
import uuid

import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow

from adapters import sqlite_cache

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
]

auth_app = flask.Flask(__name__)


@auth_app.route("/authorize")
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )

    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
    )

    webbrowser.open(authorization_url)
    return flask.redirect(authorization_url)


@auth_app.route("/oauth2callback")
def oauth2callback():
    state = flask.request.args.get("state")

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    credentials = credentials_to_dict(credentials)

    features = check_granted_scopes(credentials)

    session_id = str(uuid.uuid4())

    sqlite_cache.write(
        session_id,
        int(time.time()),
        credentials,
        features["email"],
        features["profile"],
    )

    resp = flask.make_response(
        f"Success! on future requests use header <pre><code>SESSION-ID: {session_id}</code><pre>"
    )
    resp.headers["SESSION-ID"] = session_id
    return resp


@auth_app.route("/revoke")
def revoke():
    session_id = flask.request.headers.get("SESSION-ID")
    if session_id == "":
        return "no session_id given on request headers"
    row = sqlite_cache.read(session_id)
    if row is None:
        return "session ID not found"

    credentials = google.oauth2.credentials.Credentials(**row["credentials"])

    revoke_resp = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
        timeout=60,
    )

    status_code = getattr(revoke_resp, "status_code")
    if status_code == 200:
        return f"Credentials successfully revoked. Status: {status_code}"
    else:
        return f"An error occurred. Status: {status_code}"


@auth_app.route("/clear")
def clear_credentials():
    session_id = flask.request.headers.get("SESSION-ID")
    if session_id == "":
        return "no session_id given on request headers"
    sqlite_cache.write(
        session_id, 0, {}, False, False
    )
    return "Credentials have been cleared.<br><br>"


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
    features = {}
    if (
        "https://www.googleapis.com/auth/userinfo.email"
        in credentials["granted_scopes"]
    ):
        features["email"] = True
    else:
        features["email"] = False

    if (
        "https://www.googleapis.com/auth/userinfo.profile"
        in credentials["granted_scopes"]
    ):
        features["profile"] = True
    else:
        features["profile"] = False

    return features
