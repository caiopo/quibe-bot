import requests
import bs4

from re import compile
from pytz import timezone
from datetime import datetime

spaces = compile('\s+')

def fetch():
    resp = requests.get('http://ru.ufsc.br/ru/')

    if not resp.ok:
        return []

    bs = bs4.BeautifulSoup(resp.content, 'html.parser')

    cardapio = [entry.text for entry in bs.find_all(align='center')][3:]

    weekday = datetime.now(timezone('America/Sao_Paulo')).weekday()

    today = cardapio[(weekday * 6 + 2):(weekday * 6 + 6)]

    today = [spaces.sub(' ', item.strip(' \n\xa0').replace('\n', '').replace('/', ' e ').lower())
                for item in today]

    return today
