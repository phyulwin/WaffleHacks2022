#move code to main after testing and linking with html
import json
import os
import re

from flask import Flask, redirect, render_template, session, url_for, request

app = Flask(__name__)
#go to homepage (index.hmtl)
@app.route("/")
def home():
    return render_template("index.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

#code to run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))

#if the above port is occupied, use the one below
#app.run(host='0.0.0.0', port=81)