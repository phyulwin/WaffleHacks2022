import os
import re
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisaseceret'

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ['AUTH0_CLIENT_ID'],
    client_secret=os.environ['AUTH0_CLIENT_SECRET'],
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ["AUTH0_DOMAIN"]}/.well-known/openid-configuration',
)

# Controllers API
@app.route("/")
def home():
    return render_template(
        "index.html",
        session=session.get("user"),
        subject=" ",
        #pretty=json.dumps(session.get("user"), indent=4),
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/connect", methods=["GET","POST"])
def connect():
  if request.method == 'POST':
    subject=request.form.get('subject')
    return render_template("index.html",subject=subject)
  else:
    return render_template("index.html",subject=" ")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)