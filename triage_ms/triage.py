import requests
from os import environ

VALIDATE_URL = "https://fr1gi6xdtc.execute-api.us-west-2.amazonaws.com/prod/validate"

def primaryHandler (form : dict):
   if (not validateForm(form)):
      return "Invalid Form",400
   elif (not validateRequest(form.get("username"), form.get("token"))):
      return "Invalid Login", 400
   else:
      return triageResults(form)
 
def validateForm (form : dict) -> bool:
   keys = ["username","token","pain_level","head_trauma","allergies","runny_nose","sore_throat","shortness_of_breath","inflammation","fever","cough","chest_pain","breathing_difficulty"]
   for key in keys:
      if key not in form:
        return False
   return True

def validateRequest (username : str, token: str):
   APIKEY= environ.get("API_KEY",""); # Get API key stored in environment variables or empty string
   response = requests.get(VALIDATE_URL,
                           params={"username":username,"token":token},
                           headers={"X-Api-Key":APIKEY})
   return response.status_code == 200

def triageResults (symptomInput :dict):
    
   responseData = {"result":"Futher Triage Needed",
                   "cause":"na",
                   "medicine":"na"
                  } # Default Triage Result

  # Pain Level 
   if symptomInput["pain_level"] >= 7:
        responseData["result"] = "ER"
   else:
      
      # Head Trauma
      if symptomInput["head_trauma"]:
          responseData["result"] = "Futher Triage Needed"

      # inflammation
      elif symptomInput["inflammation"] in ["moderate", "severe"]:
          responseData["result"] = "Futher Triage Needed"
          responseData["cause"] = "Possible infection"

      # Chest Pain
      elif symptomInput["chest_pain"]:
        responseData["result"] = "Futher Triage Needed"
        responseData["cause"] = "Chest Pain"

      # Breathing
      elif symptomInput["breathing_difficulty"]:
        responseData["cause"] = "Difficulty Breathing"
        responseData["result"] = "Futher Triage Needed"

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
                   responseData["result"] = "Futher Triage Needed"
   
   return responseData,200
 