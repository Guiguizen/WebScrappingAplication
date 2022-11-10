import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()

def ApagarTabela(url, delete_url):
    #Exemplo ApagarTabela('http://127.0.0.1:8000/trend-api/wsgeral/hastag', 'http://127.0.0.1:8000/trend-api/wsgeral/delete-hastag/')
    #Pega o primeiro ID da tabela
    try:
        json_var = requests.get(url).text
        inp_dict = json.loads(str(json_var))
        ultimo_id = (inp_dict[0]['id'])  
        link = delete_url+str(ultimo_id)
        r = requests.get(link)
    except:
        try:
            print("DELETE Error at"+link)
        except:
            print("Default DELETE Error")

#ApagarTabela('https://trendy-tiktok-api.herokuapp.com/trend-api/wsgeral/hastag', 'https://trendy-tiktok-api.herokuapp.com/trend-api/wsgeral/delete-hastag/')