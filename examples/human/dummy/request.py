import requests
import json

def predict(data):
    url = "http://127.0.0.1:5000/predict"
    payload=data
    files=[

    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.json()['result']