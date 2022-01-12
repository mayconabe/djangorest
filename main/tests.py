from django.test import TestCase
import requests
import json


URL = 'http://127.0.0.1:8000/'

response = requests.post(URL+'api-token/', data={'username': 'mayconabe', 'password': 'carro123'})
print(response.text)
response_dict = json.loads(response.text)
# print(response_dict['token'])
token = response_dict['token']

usuarios = []
next_ = URL+'main/usuarios/'
count = 0

while next_:
    count += 1

    response = requests.get(next_, headers={'Authorization': 'Token ' + token})
    print(response.text)
    print(response.status_code)



    if response.status_code == 200:
        response_dict = json.loads(response.text)

        for i in response_dict['results']:
            usuarios.append(i)

        if 'next' in response_dict:
            next_ = response_dict['next']
    print(count, next_)

for usuario in usuarios:
    print(usuario['nome'])