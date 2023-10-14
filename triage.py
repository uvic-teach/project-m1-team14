from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os
import json
from os import environ

app = Flask(name, static_folder='staticFiles')


@app.route("/")
def index():
    return "";

triageSymptoms = {
  "pain_level": 1,
  "physical_pain": False,
  "headache": True,
  "sore_throat": False,
  "runny_nose": True,
  "allergies": False,
  "inflamation": "none",
  "head_trauma": False
}

@app.route('/triage')
def triage():
    if (triageSymptoms["head_trauma"] == True):
        return "go to ER, there is a threat to your life"
    elif(triageSymptoms["allergies"] == True):
        return "OTC drugs"
    elif(triageSymptoms["inflamation"] or triageSymptoms["physical_pain"]):
        return "Plesae visit a GP in person"

    return "Further in person triage necessary to determine results"

@app.route('/test')
def test():
    return "test"

if name == 'main':
    app.run(host="0.0.0.0", port=4000, debug=True)
