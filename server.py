#move code to main after testing and linking with html
import json
import os
import re

from os import environ as env
from urllib.parse import quote_plus, urlencode
from flask_socketio import SocketIO, send
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request
'''
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
'''
app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ["AUTH0_CLIENT_ID"],
    client_secret=os.environ["AUTH0_CLIENT_SECRET"],
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
)

sectio = SocketIO(app, cors_allowed_origins = "*")

@socketio.on('message')
def handle_message(message):
  print("message: " + message)
  if( message != "{} Connected!"):
    send(message, broadcast=True)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ['AUTH0_DOMAIN']
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.environ['AUTH0_CLIENT_ID'],
            },
            quote_via=quote_plus,
        )
    )

#go to homepage (index.hmtl)
@app.route("/")
def home():
    return render_template("index.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/connect')
def create():
  return render_template('connect.html')
  
#code to run server
if __name__ == "__main__":
  
    app.run(host='0.0.0.0', port=81)

#if the above port is occupied, use the one below
#app.run(host='0.0.0.0', port=81)