import requests
import bs4

from re import compile
from pytz import timezone
from datetime import datetime

spaces = compile('\s+')


def sanitize(string):
    return spaces.sub(' ', (string.strip(' \n\xa0').replace('\n', '')
                            .replace('/', ' e ').lower()))


def fetch():
    resp = requests.get('http://ru.ufsc.br/ru/')

    if not resp.ok:
        return []

    soup = bs4.BeautifulSoup(resp.content, 'lxml')

    cardapio = [entry.text for entry in soup.find_all(align='center')][3:]

    weekday = datetime.now(timezone('America/Sao_Paulo')).weekday()

    today = cardapio[(weekday * 6 + 2):(weekday * 6 + 6)]

    today = [sanitize(item) for item in today]

    return today
