# READ ENVIRONMENT VARIABLES
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# IMPORT DEPENDENCIES
import json, os
import requests

from flask import Flask, request, render_template

SEARCH_NLU_ENDPOINT = os.getenv("SEARCH_NLU_ENDPOINT")

# CREATE FLASK SERVER
app = Flask("frontend-flask")

# Main page
@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def search():
    print("Received call to /search endpoint")
    # collecting parametes
    url_to_search = request.form["webpage"]
    print("url to search:",url_to_search)
    # send request to search-nlu
    payload = json.dumps({
        "url": url_to_search
    })
    headers = {'Content-Type': 'application/json'}
    nlu_results_raw = requests.request("POST",SEARCH_NLU_ENDPOINT, headers=headers, data=payload)
    nlu_results = nlu_results_raw.json()
    print(nlu_results)
    # return results
    results_page = "<h1>Results</h1>"
    results_page += "<p>Within the selected webpage I have extracted the following keywords</p>"
    results_page += "<p>"
    for keyword in nlu_results['results']:
        results_page += keyword + "</br>"
    results_page += "</p>"
    results_page += "<a href=\"/\">Return to homepage</a>"
    return results_page

# Healthcheck
@app.route("/health", methods=["GET"])
def healthcheck():
    return {"status": "healthy"}

####################################
########### LOGIN ##################

# example login (outdated, using a previous version of flask-login): https://pythonbasics.org/flask-login/
# documentation: https://flask-login.readthedocs.io/en/latest/

from flask_login import LoginManager, login_user

from UserModel import User #import user model

login_manager = LoginManager()
login_manager.init_app(app)

# Login page
@app.route("/login", methods=["GET"])
def loginpage():
    return render_template("login.html")


####################################


app.run(host='0.0.0.0', port=8080)