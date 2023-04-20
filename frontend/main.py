# READ ENVIRONMENT VARIABLES
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# IMPORT DEPENDENCIES
import json, os

from flask import Flask, request, render_template

# CREATE FLASK SERVER
app = Flask("frontend-flask")

# Main page
@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")

# Healthcheck
@app.route("/health", methods=["GET"])
def healthcheck():
    return {"status": "healthy"}

app.run(host='0.0.0.0', port=8080)