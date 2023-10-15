#openapi: 3.0.0
#info:
#version: "1.0.0"
#title: TraigeMS
#description: The API to determine Triage results based on a form

import os,json

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
  
    #     sample request body:
    #     {
    #     "pain_level":9,
    #     "head_trauma":false,
    #     "allergies":true,
    #     "runny_nose":true,
    #     "sore_throat":true,
    #     "shortness_of_breath":true,
    #     "inflammation":"mild",
    #     "fever":true,
    #     "cough":true,
    #     "chest_pain":true,
    #     "breathing_difficulty":true
    # }
    
    #     responses:
    #       200:
    #         description: return triage in the form of a 3 key-value pair dictionary
    
   symptomInput = request.json # JSON Body
   responseData = {"result":"Further Triage Needed",
                   "cause":"na",
                   "medicine":"na"
                  } # Default Triage Result

  # Pain Level 
   if symptomInput["pain_level"] >= 7:
        responseData["result"] = "ER"
   else:
      
      # Head Trauma
      if symptomInput["head_trauma"]:
          responseData["result"] = "Further Triage Needed"

      # inflammation
      elif symptomInput["inflammation"] in ["moderate", "severe"]:
          responseData["result"] = "Further Triage Needed"
          responseData["cause"] = "Possible infection"

      # Chest Pain
      elif symptomInput["chest_pain"]:
        responseData["result"] = "Further Triage Needed"
        responseData["cause"] = "Chest Pain"

      # Breathing
      elif symptomInput["breathing_difficulty"]:
        responseData["cause"] = "Difficulty Breathing"
        responseData["result"] = "Further Triage Needed"

      # Allergy Symptoms
      elif symptomInput["allergies"]:
          if symptomInput["runny_nose"] and symptomInput["sore_throat"]:
              responseData["cause"] = "Possible Seasonal Allergies"
              responseData["result"] = "Over the counter Medicine"
              responseData["medicine"] = "Antihistamines"

          elif symptomInput["shortness_of_breath"]:
              responseData["cause"] = "Possible Allergy Reaction"
              responseData["result"] = "ER"
      
      # Generic Cold Symptoms
      else:
          if symptomInput["fever"]:
            if symptomInput["cough"]:
                responseData["cause"] = "Possible Cold / Flu"
                responseData["result"] = "Over the counter Medicine"
                responseData["medicine"] = "Cold FX"
            else:
                if symptomInput["runny_nose"]:
                   responseData["cause"] = "Common Cold"
                   responseData["result"] = "Over the counter Medicine"
                   responseData["medicine"] = "Cold Medicine"
                else:
                   responseData["cause"] = "Possible Infection"
                   responseData["result"] = "Further Triage Needed"
            

   return responseData


if __name__ == '__main__':
   app.run()
