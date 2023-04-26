# READ ENVIRONMENT VARIABLES
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# IMPORT DEPENDENCIES
import json, os
import requests

from flask import Flask, request, render_template, redirect, session
from flask_login import LoginManager, login_user, logout_user, login_required


SEARCH_NLU_ENDPOINT = os.getenv("SEARCH_NLU_ENDPOINT")

AUTHENTICATION_USERNAME = os.getenv("AUTH_USERNAME")
AUTHENTICATION_PASSWORD = os.getenv("AUTH_PASSWORD")

# CREATE FLASK SERVER
app = Flask("frontend-flask")

# Main page
@app.route("/", methods=["GET"])
@login_required
def homepage():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
@login_required
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

from UserModel import User #import user model
tester = User()

login_manager = LoginManager()
login_manager.init_app(app)

# setup a unique and not disclosed value for the secret of the session
app.secret_key = os.getenv("SESSION_SECRET")


# tell flask how to retrieve the user
@login_manager.user_loader
def load_user(user_id):
    print("checking if user is logged in",user_id,tester.get_id())
    if tester.get_id() == user_id:
        print("user is logged in")
        return tester
    else:
        print("user is NOT logged in")
        return None

# tell flask what to do if a user that is NOT authenticated tries to access a protected page
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

# Login page
@app.route("/login", methods=["GET"])
def loginpage():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    # collect login parameters of the user
    form_username = request.form['username']
    form_password = request.form['password']

    print("user tried to login:",form_username,form_password)
    

    # check if the username and password are correct
    if form_username == AUTHENTICATION_USERNAME and form_password == AUTHENTICATION_PASSWORD:
        # log in the user
        # .....
        print("username and password correct, logging in the user")
        session['username'] = form_username
        login_user(tester)
        # redirect the user to the / main page
        return redirect("/")

    else:
        # user is not authorized
        print("username and password not correct")
        # redirect the user to the /login page
        return redirect("/login")

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    session.pop('username', None)
    session['logged_in']=False
    return redirect("/login")

####################################


app.run(host='0.0.0.0', port=8080)