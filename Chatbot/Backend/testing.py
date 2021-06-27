

import requests

url = "https://andruxnet-world-cities-v1.p.rapidapi.com/"

querystring = {"query":"tamil nadu","searchby":"city"}

headers = {
    'x-rapidapi-key': "15661f3c28msh5bfba6aef2aed8ep170deejsna8eeabb092ac",
    'x-rapidapi-host': "andruxnet-world-cities-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

  