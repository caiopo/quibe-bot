import requests
from os import environ

resp = requests.get('https://' + environ['APP_NAME'] + '.herokuapp.com/')

print(resp.status_code)
