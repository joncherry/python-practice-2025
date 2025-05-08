# -*- coding: utf-8 -*-

import os
import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow

CLIENT_SECRETS_FILE = "client_secret.json"

# Scopes to request user info (email, profile)
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
USER_INFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/userinfo'

app = flask.Flask(__name__)
app.secret_key = 'REPLACE_ME_WITH_A_SECRET_KEY'

@app.route('/')
def index():
    if 'user_info' in flask.session:
        user = flask.session['user_info']
        return f"Signed in as: {user['email']}<br>Name: {user['name']}<br><a href='/clear'>Logout</a>"
    return '<a href="/authorize">Sign in with Google</a>'

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    flask.session['state'] = state
    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    flow.fetch_token(authorization_response=flask.request.url)
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    # Fetch user info to confirm login
    user_info = requests.get(USER_INFO_ENDPOINT, headers={
        'Authorization': f'Bearer {credentials.token}'
    }).json()

    flask.session['user_info'] = user_info

    return flask.redirect('/')

@app.route('/clear')
def clear_credentials():
    flask.session.clear()
    return 'You have been logged out.<br><br><a href="/">Return</a>'

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    app.run('localhost', 8080, debug=True)
