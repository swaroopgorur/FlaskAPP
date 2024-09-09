import requests
import json
from flask_app.config import Config
import re

############################################################################################
######################################## Mask API key ######################################
############################################################################################

def mask_api_key(url):
    return re.sub(r'key=[\w-]+', 'key=HIDDEN', url)

############################################################################################
########################## Text Analysis using Perspective API #############################
############################################################################################

def analyze_content(text):
    api_key = Config.PERSPECTIVE_API_KEY
    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }
    
    try:
        print(f"Sending request to: {mask_api_key(api_url)}")
        print(f"Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(api_url, json=data)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text}")
        
        response.raise_for_status()
        
        if not response.text:
            print("Empty response received from the API")
            return None
        
        result = response.json()
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        print(f"Response content: {response.text}")
        return None

############################################################################################
########################## Content Appropriateness Check ###################################
############################################################################################

def is_content_appropriate(analysis_result):
    if analysis_result is None:
        return False
    
    try:
        toxicity_score = analysis_result['attributeScores']['TOXICITY']['summaryScore']['value']
        insult_score = analysis_result['attributeScores']['INSULT']['summaryScore']['value']
        profanity_score = analysis_result['attributeScores']['PROFANITY']['summaryScore']['value']
        threat_score = analysis_result['attributeScores']['THREAT']['summaryScore']['value']
        
        print(f"Toxicity: {toxicity_score}, Insult: {insult_score}, Profanity: {profanity_score}, Threat: {threat_score}")
        
        return all(score < 0.75 for score in [toxicity_score, insult_score, profanity_score, threat_score])
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        print(json.dumps(analysis_result, indent=2))
        return False
    

############################################################################################
########################################### END ############################################
############################################################################################