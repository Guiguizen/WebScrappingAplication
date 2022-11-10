import requests
import os

DJANGO_API_URL='https://trendy-tiktok-api.herokuapp.com/trend-api/'

data={
    "hastag": "aaaa",
    "position": "1",
}


r = requests.post(DJANGO_API_URL+'wsgeral/hastag', json=data)

#print(r.text)

json_var = requests.get('https://trendy-tiktok-api.herokuapp.com/trend-api/'+'wsgeral/creator').text

print(json_var)