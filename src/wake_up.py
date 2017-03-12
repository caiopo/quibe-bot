import requests
from os import environ

requests.get('https://' + environ['APP_NAME'] + '.herokuapp.com/')
