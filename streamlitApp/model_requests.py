import requests, json

def generate_response(domain, user_pref, past_contributions):
   url = "http://localhost:8989/issue_matcha/recommend"
   payload = { 
       "domain": str(domain),
       "user_pref": user_pref,
       "past_contributions": past_contributions
   }
   headers = {
       "accept": "application/json",
       "content-type": "application/json"
   }

   response = requests.post(url, json=payload, headers=headers)
   return response.json()

# def generate_response(prompt):
#    url = "https://api.fireworks.ai/inference/v1/chat/completions"
#    payload = { 
#        "messages": [
#            {
#                "role": "user",
#                "content": prompt
#            }
#        ],
#        "max_tokens": 1024,
#        "temperature": 0.01,
#        "frequency_penalty": 0,
#        "presence_penalty": 0,
#        "n": 1,
#        "stop": None,
#        "response_format": { "type": "json_object" },
#        "model": "accounts/fireworks/models/mixtral-8x7b-instruct",
#        "stream": False
#    }
#    headers = {
#        "accept": "application/json",
#        "content-type": "application/json",
#        "authorization": f"Bearer {}"
#    }


#    response = requests.post(url, json=payload, headers=headers)
#    return response.json()


def generate_mistral_response(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = { 
       "messages": [
           {
               "role": "user",
               "content": prompt
           }
       ],
       "max_tokens": 1024,
       "temperature": 0.01,
       "model": "mistral-large-latest",
   }
    headers = {
       "accept": "application/json",
       "content-type": "application/json",
       "authorization": f"Bearer {}"
    }


    response = requests.post(url, json=payload, headers=headers)
    return response.json()
