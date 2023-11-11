#openapi: 3.0.0
#info:
# version: "1.0.0"
#  title: TraigeMS
#description: The API to determine Triage results based on a form

import os,json
from os import environ
from triage import primaryHandler
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/triage', methods=["POST"])
def triageSymptoms():
    
    # Processes the form answers in JSON format and returns traige result
    #     ---
    #     post:
    #       description: sends the form answers in json format to the flask server to determine triage result

    #     responses:
    #       200:
    #         description: return triage  in the form of a 3 key dictionary
   symptomInput = request.json # JSON Body
   response = primaryHandler(symptomInput)

   return response


@app.route('/heartbeat')
def heartbeat():
   return "End point reachable!",200

if __name__ == '__main__':
   app.run()
